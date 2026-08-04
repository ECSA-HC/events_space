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
    header('Location: poster_score.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Require authenticated poster scoring session
|--------------------------------------------------------------------------
*/

$judgeId = (int) (
    $_SESSION['judge_id'] ?? 0
);

$presenterId = (int) (
    $_SESSION['selected_presenter_id'] ?? 0
);

$selectedPresentationType = (string) (
    $_SESSION['selected_presentation_type'] ?? ''
);

if ($judgeId < 1) {
    $_SESSION['error'] =
        'Your session has expired. Please enter your email again.';

    header('Location: email.php');
    exit;
}

if ($selectedPresentationType !== 'poster') {
    $_SESSION['error'] =
        'Please select poster presentation before continuing.';

    header('Location: select_presentation_type.php');
    exit;
}

if ($presenterId < 1) {
    $_SESSION['error'] =
        'Please select a poster presenter before submitting a score.';

    header('Location: select_poster_presenter.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Validate CSRF token
|--------------------------------------------------------------------------
*/

$csrfToken = (string) (
    $_POST['csrf_token'] ?? ''
);

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

    header('Location: poster_score.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Load active poster criteria
|--------------------------------------------------------------------------
*/

try {
    $statement = $pdo->query(
        'SELECT
            id,
            name,
            weight_percent
         FROM poster_criteria
         WHERE is_active = 1
         ORDER BY display_order ASC, id ASC'
    );

    $criteria = $statement->fetchAll(PDO::FETCH_ASSOC);

    if ($criteria === []) {
        throw new RuntimeException(
            'No active poster scoring criteria are configured.'
        );
    }

    $totalWeight = 0.0;

    foreach ($criteria as $criterion) {
        $totalWeight += (float) $criterion['weight_percent'];
    }

    if (abs($totalWeight - 100.0) > 0.001) {
        throw new RuntimeException(
            'Poster scoring criterion weights must total 100%.'
        );
    }
} catch (Throwable $exception) {
    error_log(
        'Poster scoring criteria loading failed: '
        . $exception->getMessage()
    );

    $_SESSION['error'] =
        'Poster scoring criteria could not be loaded. '
        . 'Please contact the administrator.';

    header('Location: poster_score.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Read submitted criterion scores
|--------------------------------------------------------------------------
*/

$submittedCriterionScores = $_POST['criterion'] ?? [];

if (!is_array($submittedCriterionScores)) {
    $submittedCriterionScores = [];
}

$submittedScores = [];
$validationErrors = [];

/*
|--------------------------------------------------------------------------
| Validate criterion scores
|--------------------------------------------------------------------------
*/

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
| Retain form values after validation failure
|--------------------------------------------------------------------------
*/

$_SESSION['old_poster_scores'] =
    $submittedScores;

$_SESSION['old_poster_comments'] =
    $comments;

if ($validationErrors !== []) {
    $_SESSION['error'] = implode(
        ' ',
        $validationErrors
    );

    header('Location: poster_score.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Calculate weighted overall poster score
|--------------------------------------------------------------------------
*/

$overallScore = 0.0;

foreach ($criteria as $criterion) {
    $criterionId = (int) $criterion['id'];
    $weightPercent = (float) $criterion['weight_percent'];
    $scoreValue = $submittedScores[$criterionId];

    $overallScore +=
        $scoreValue * ($weightPercent / 100);
}

$overallScore = round(
    $overallScore,
    2
);

/*
|--------------------------------------------------------------------------
| Save poster score transaction
|--------------------------------------------------------------------------
*/

try {
    $pdo->beginTransaction();

    /*
     * Verify that the presenter exists, is active, and is a poster
     * presenter.
     */
    $statement = $pdo->prepare(
        'SELECT id
         FROM presenters
         WHERE id = :presenter_id
           AND presentation_type = :presentation_type
           AND is_active = 1
         LIMIT 1
         FOR UPDATE'
    );

    $statement->execute([
        'presenter_id' => $presenterId,
        'presentation_type' => 'poster',
    ]);

    if ($statement->fetchColumn() === false) {
        throw new RuntimeException(
            'The selected poster presenter is not available.'
        );
    }

    /*
     * Prevent the same judge from scoring the same poster twice.
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
            $_SESSION['old_poster_scores'],
            $_SESSION['old_poster_comments']
        );

        $_SESSION['error'] =
            'You have already submitted a score for this poster presentation.';

        header('Location: select_poster_presenter.php');
        exit;
    }

    /*
     * Create the main score record.
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
     * Save each poster criterion score.
     */
    $statement = $pdo->prepare(
        'INSERT INTO poster_score_items
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

    /*
     * Clear retained form values.
     */
    unset(
        $_SESSION['old_poster_scores'],
        $_SESSION['old_poster_comments'],
        $_SESSION['error']
    );

    /*
     * Store success state for poster_score.php.
     */
    $_SESSION['poster_score_submitted'] = true;

    $_SESSION['last_poster_overall_score'] =
        $overallScore;

    /*
     * Rotate CSRF token after successful submission.
     */
    $_SESSION['csrf_token'] =
        bin2hex(random_bytes(32));

    header('Location: poster_score.php');
    exit;
} catch (Throwable $exception) {
    if ($pdo->inTransaction()) {
        $pdo->rollBack();
    }

    error_log(
        'Poster score submission failed: '
        . $exception->getMessage()
    );

    $_SESSION['error'] =
        'Your poster score could not be submitted. Please try again.';

    header('Location: poster_score.php');
    exit;
}