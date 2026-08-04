<?php
declare(strict_types=1);

session_start();

require_once __DIR__ . '/includes/database.php';

/*
|--------------------------------------------------------------------------
| Allow POST requests only
|--------------------------------------------------------------------------
*/

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Location: score.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Require authenticated scoring session
|--------------------------------------------------------------------------
*/

$judgeId = (int) ($_SESSION['judge_id'] ?? 0);
$subthemeId = (int) ($_SESSION['selected_subtheme_id'] ?? 0);
$presenterId = (int) ($_SESSION['selected_presenter_id'] ?? 0);

if ($judgeId < 1) {
    $_SESSION['error'] =
        'Your session has expired. Please enter your email again.';

    header('Location: email.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Require oral presentation flow
|--------------------------------------------------------------------------
*/

if (
    ($_SESSION['selected_presentation_type'] ?? '') !== 'oral'
) {
    header('Location: select_presentation_type.php');
    exit;
}

if ($subthemeId < 1) {
    $_SESSION['error'] =
        'Please select a sub-theme before submitting a score.';

    header('Location: select_subtheme.php');
    exit;
}

if ($presenterId < 1) {
    $_SESSION['error'] =
        'Please select a presenter before submitting a score.';

    header('Location: select_presenter.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Validate CSRF token
|--------------------------------------------------------------------------
*/

$csrfToken = (string) ($_POST['csrf_token'] ?? '');

if (
    $csrfToken === '' ||
    empty($_SESSION['csrf_token']) ||
    !hash_equals(
        (string) $_SESSION['csrf_token'],
        $csrfToken
    )
) {
    $_SESSION['error'] =
        'Your session has expired. Please submit the scoring form again.';

    header('Location: score.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Load active criteria from database
|--------------------------------------------------------------------------
*/

try {
    $statement = $pdo->query(
        'SELECT
            id,
            name,
            weight_percent
         FROM criteria
         WHERE is_active = 1
         ORDER BY display_order ASC, id ASC'
    );

    $criteria = $statement->fetchAll(PDO::FETCH_ASSOC);

    if ($criteria === []) {
        throw new RuntimeException(
            'No active scoring criteria have been configured.'
        );
    }

    $totalWeight = 0;

    foreach ($criteria as $criterion) {
        $totalWeight += (int) $criterion['weight_percent'];
    }

    if ($totalWeight !== 100) {
        throw new RuntimeException(
            'Active scoring criterion weights must total 100%.'
        );
    }
} catch (Throwable $exception) {
    error_log(
        'Scoring criteria loading failed: '
        . $exception->getMessage()
    );

    $_SESSION['error'] =
        'The scoring criteria could not be loaded. Please contact the administrator.';

    header('Location: score.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Read and validate submitted scores
|--------------------------------------------------------------------------
*/

$submittedCriterionScores = $_POST['criterion'] ?? [];

if (!is_array($submittedCriterionScores)) {
    $submittedCriterionScores = [];
}

$submittedScores = [];
$validationErrors = [];

foreach ($criteria as $criterion) {
    $criterionId = (int) $criterion['id'];
    $criterionName = (string) $criterion['name'];

    $rawScore = trim(
        (string) (
            $submittedCriterionScores[$criterionId] ?? ''
        )
    );

    if (
        $rawScore === '' ||
        preg_match('/^\d{1,3}$/', $rawScore) !== 1
    ) {
        $validationErrors[] =
            $criterionName
            . ' must be a whole number from 0 to 100.';

        continue;
    }

    $scoreValue = (int) $rawScore;

    if ($scoreValue < 0 || $scoreValue > 100) {
        $validationErrors[] =
            $criterionName
            . ' must be between 0 and 100.';

        continue;
    }

    $submittedScores[$criterionId] = $scoreValue;
}

/*
|--------------------------------------------------------------------------
| Validate comments
|--------------------------------------------------------------------------
*/

$comments = trim(
    (string) ($_POST['comments'] ?? '')
);

if (mb_strlen($comments) > 1000) {
    $validationErrors[] =
        'Comments must not exceed 1,000 characters.';
}

/*
|--------------------------------------------------------------------------
| Retain submitted values after validation failure
|--------------------------------------------------------------------------
*/

$_SESSION['old_scores'] = $submittedScores;
$_SESSION['old_comments'] = $comments;

if ($validationErrors !== []) {
    $_SESSION['error'] = implode(
        ' ',
        $validationErrors
    );

    header('Location: score.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Calculate weighted overall score
|--------------------------------------------------------------------------
*/

$overallScore = 0.0;

foreach ($criteria as $criterion) {
    $criterionId = (int) $criterion['id'];
    $weightPercent = (int) $criterion['weight_percent'];
    $scoreValue = $submittedScores[$criterionId];

    $overallScore +=
        $scoreValue * ($weightPercent / 100);
}

$overallScore = round($overallScore, 2);

/*
|--------------------------------------------------------------------------
| Save score transaction
|--------------------------------------------------------------------------
*/

try {
    $pdo->beginTransaction();

    /*
     * Verify that the presenter exists, is active, belongs to
     * the selected sub-theme, and is an oral presentation.
     */
    $statement = $pdo->prepare(
        'SELECT id
         FROM presenters
         WHERE id = :presenter_id
           AND subtheme_id = :subtheme_id
           AND presentation_type = :presentation_type
           AND is_active = 1
         LIMIT 1
         FOR UPDATE'
    );

    $statement->execute([
        'presenter_id' => $presenterId,
        'subtheme_id' => $subthemeId,
        'presentation_type' => 'oral',
    ]);

    if ($statement->fetchColumn() === false) {
        throw new RuntimeException(
            'The selected presenter is not available.'
        );
    }

    /*
     * Prevent duplicate scoring.
     */
    $statement = $pdo->prepare(
        'SELECT id
         FROM scores
         WHERE judge_id = :judge_id
           AND presenter_id = :presenter_id
         LIMIT 1
         FOR UPDATE'
    );

    $statement->execute([
        'judge_id' => $judgeId,
        'presenter_id' => $presenterId,
    ]);

    if ($statement->fetchColumn() !== false) {
        $pdo->rollBack();

        unset(
            $_SESSION['old_scores'],
            $_SESSION['old_comments']
        );

        $_SESSION['error'] =
            'You have already submitted a score for this presentation.';

        header('Location: select_presenter.php');
        exit;
    }

    /*
     * Create main score record.
     */
    $statement = $pdo->prepare(
        'INSERT INTO scores
        (
            judge_id,
            presenter_id,
            overall_score,
            comments
        )
        VALUES
        (
            :judge_id,
            :presenter_id,
            :overall_score,
            :comments
        )'
    );

    $statement->execute([
        'judge_id' => $judgeId,
        'presenter_id' => $presenterId,
        'overall_score' => $overallScore,
        'comments' => $comments !== ''
            ? $comments
            : null,
    ]);

    $scoreId = (int) $pdo->lastInsertId();

    /*
     * Save each criterion score.
     */
    $statement = $pdo->prepare(
        'INSERT INTO score_items
        (
            score_id,
            criterion_id,
            score_value
        )
        VALUES
        (
            :score_id,
            :criterion_id,
            :score_value
        )'
    );

    foreach ($criteria as $criterion) {
        $criterionId = (int) $criterion['id'];

        $statement->execute([
            'score_id' => $scoreId,
            'criterion_id' => $criterionId,
            'score_value' => $submittedScores[$criterionId],
        ]);
    }

    $pdo->commit();

    unset(
        $_SESSION['old_scores'],
        $_SESSION['old_comments'],
        $_SESSION['error']
    );

    $_SESSION['score_submitted'] = true;
    $_SESSION['last_overall_score'] = $overallScore;

    /*
     * Rotate CSRF token after successful submission.
     */
    $_SESSION['csrf_token'] = bin2hex(
        random_bytes(32)
    );

    header('Location: score.php');
    exit;
} catch (Throwable $exception) {
    if ($pdo->inTransaction()) {
        $pdo->rollBack();
    }

    error_log(
        'Score submission failed: '
        . $exception->getMessage()
    );

    $_SESSION['error'] =
        'Your score could not be submitted. Please try again.';

    header('Location: score.php');
    exit;
}