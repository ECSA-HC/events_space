<?php
declare(strict_types=1);

session_start();

require_once __DIR__ . '/includes/database.php';

/*
|--------------------------------------------------------------------------
| Require judge authentication
|--------------------------------------------------------------------------
*/

if (
    empty($_SESSION['judge_id']) ||
    empty($_SESSION['judge_email'])
) {
    $_SESSION['error'] =
        'Please enter your registered email address before continuing.';

    header('Location: email.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Require poster scoring flow
|--------------------------------------------------------------------------
*/

$judgeId = (int) ($_SESSION['judge_id'] ?? 0);

$selectedPresentationType = (string) (
    $_SESSION['selected_presentation_type'] ?? ''
);

$selectedPresenterId = (int) (
    $_SESSION['selected_presenter_id'] ?? 0
);

if ($selectedPresentationType !== 'poster') {
    $_SESSION['error'] =
        'Please select poster presentation before continuing.';

    header('Location: select_presentation_type.php');
    exit;
}

if ($selectedPresenterId < 1) {
    $_SESSION['error'] =
        'Please select a poster presenter before scoring.';

    header('Location: select_poster_presenter.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Generate CSRF token
|--------------------------------------------------------------------------
*/

if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

/*
|--------------------------------------------------------------------------
| Load poster scoring criteria
|--------------------------------------------------------------------------
*/

try {
    $statement = $pdo->query(
        'SELECT
            id,
            name,
            description,
            display_order,
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
            'Poster scoring weights must total 100%.'
        );
    }
} catch (Throwable $exception) {
    error_log(
        'Poster criteria loading failed: '
        . $exception->getMessage()
    );

    $_SESSION['error'] =
        'Poster scoring criteria could not be loaded. '
        . 'Please contact the administrator.';

    header('Location: select_poster_presenter.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Load selected poster presenter
|--------------------------------------------------------------------------
*/

try {
    $statement = $pdo->prepare(
        'SELECT
            id,
            presenter_name,
            institution,
            presentation_title,
            presentation_type
         FROM presenters
         WHERE id = :presenter_id
           AND presentation_type = :presentation_type
           AND is_active = 1
         LIMIT 1'
    );

    $statement->execute([
        'presenter_id' => $selectedPresenterId,
        'presentation_type' => 'poster',
    ]);

    $presenter = $statement->fetch(PDO::FETCH_ASSOC);

    if ($presenter === false) {
        unset(
            $_SESSION['selected_presenter_id'],
            $_SESSION['selected_presenter_name'],
            $_SESSION['selected_presenter_institution'],
            $_SESSION['selected_presentation_title']
        );

        $_SESSION['error'] =
            'The selected poster presenter is no longer available.';

        header('Location: select_poster_presenter.php');
        exit;
    }

    /*
     * Check whether this judge has already scored the poster.
     */
    $statement = $pdo->prepare(
        'SELECT id
         FROM scores
         WHERE judge_id = :judge_id
           AND presenter_id = :presenter_id
         LIMIT 1'
    );

    $statement->execute([
        'judge_id' => $judgeId,
        'presenter_id' => $selectedPresenterId,
    ]);

    $existingScoreId = $statement->fetchColumn();

    $scoreSubmitted = !empty(
        $_SESSION['poster_score_submitted']
    );

    if (
        $existingScoreId !== false &&
        !$scoreSubmitted
    ) {
        $_SESSION['error'] =
            'You have already submitted a score for this poster presentation.';

        header('Location: select_poster_presenter.php');
        exit;
    }
} catch (PDOException $exception) {
    error_log(
        'Poster score page loading failed: '
        . $exception->getMessage()
    );

    $_SESSION['error'] =
        'The poster scoring form could not be loaded. Please try again.';

    header('Location: select_poster_presenter.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Retrieve flash values
|--------------------------------------------------------------------------
*/

$error = (string) ($_SESSION['error'] ?? '');

$oldScores = is_array(
    $_SESSION['old_poster_scores'] ?? null
)
    ? $_SESSION['old_poster_scores']
    : [];

$oldComments = (string) (
    $_SESSION['old_poster_comments'] ?? ''
);

$scoreSubmitted = !empty(
    $_SESSION['poster_score_submitted']
);

$submittedOverallScore = isset(
    $_SESSION['last_poster_overall_score']
)
    ? (float) $_SESSION['last_poster_overall_score']
    : null;

unset(
    $_SESSION['error'],
    $_SESSION['old_poster_scores'],
    $_SESSION['old_poster_comments'],
    $_SESSION['poster_score_submitted'],
    $_SESSION['last_poster_overall_score']
);
?>

<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1, viewport-fit=cover"
    >

    <meta
        name="description"
        content="Score the selected poster presentation."
    >

    <meta
        name="theme-color"
        content="#06124F"
    >

    <title>
        Score Poster Presentation | Best Practices Forum Score Card
    </title>
<link rel="icon" href="assets/favicon/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="assets/favicon/favicon-16x16.png">
<link rel="apple-touch-icon" href="assets/favicon/apple-touch-icon.png">
<link rel="manifest" href="assets/favicon/site.webmanifest">
    <link
        rel="stylesheet"
        href="assets/css/bootstrap.min.css"
    >

    <link
        rel="stylesheet"
        href="assets/font/bootstrap-icons.min.css"
    >

    <link
        rel="stylesheet"
        href="assets/css/app.css"
    >

</head>

<body>

<main class="bpf-screen">

    <section
        class="bpf-card bpf-card-full"
        aria-labelledby="bpf-page-title"
    >

        <?php

        $backLink = 'select_poster_presenter.php';

        include __DIR__ . '/includes/app_header.php';

        ?>

        <div class="bpf-content bpf-score-content">

            <p class="bpf-step-label">
                Poster Scoring
            </p>

            <h1
                id="bpf-page-title"
                class="bpf-title"
            >
                Score Poster
            </h1>

            <p class="bpf-description">
                Enter a score from 0 to 100 for each criterion.
            </p>

            <section
                class="bpf-score-presentation"
                aria-label="Selected poster presentation"
            >

                <div class="bpf-score-presentation-theme">

                    <i
                        class="bi bi-easel-fill"
                        aria-hidden="true"
                    ></i>

                    <span>
                        Poster Presentation
                    </span>

                </div>

                <h2>
                    <?= htmlspecialchars(
                        (string) $presenter['presentation_title'],
                        ENT_QUOTES,
                        'UTF-8'
                    ) ?>
                </h2>

                <div class="bpf-score-presenter">

                    <i
                        class="bi bi-person-fill"
                        aria-hidden="true"
                    ></i>

                    <span>
                        <?= htmlspecialchars(
                            (string) $presenter['presenter_name'],
                            ENT_QUOTES,
                            'UTF-8'
                        ) ?>
                    </span>

                </div>

                <?php if (
                    trim(
                        (string) ($presenter['institution'] ?? '')
                    ) !== ''
                ): ?>

                    <p>
                        <?= htmlspecialchars(
                            (string) $presenter['institution'],
                            ENT_QUOTES,
                            'UTF-8'
                        ) ?>
                    </p>

                <?php endif; ?>

            </section>

            <?php if ($error !== ''): ?>

                <div
                    class="alert alert-danger bpf-alert"
                    role="alert"
                >
                    <?= htmlspecialchars(
                        $error,
                        ENT_QUOTES,
                        'UTF-8'
                    ) ?>
                </div>

            <?php endif; ?>

            <?php if (!$scoreSubmitted): ?>

                <form
                    action="submit_poster_score.php"
                    method="post"
                    class="bpf-form bpf-score-form"
                    id="bpf-score-form"
                    novalidate
                >

                    <input
                        type="hidden"
                        name="csrf_token"
                        value="<?= htmlspecialchars(
                            (string) $_SESSION['csrf_token'],
                            ENT_QUOTES,
                            'UTF-8'
                        ) ?>"
                    >

                    <fieldset class="bpf-score-fieldset">

                        <legend class="visually-hidden">
                            Poster presentation scoring criteria
                        </legend>

                        <?php foreach (
                            $criteria as $index => $criterion
                        ): ?>

                            <?php
                            $criterionId =
                                (int) $criterion['id'];

                            $inputId =
                                'poster-criterion-' . $criterionId;

                            $oldValue = isset(
                                $oldScores[$criterionId]
                            )
                                ? (string) $oldScores[$criterionId]
                                : '';
                            ?>

                            <div class="bpf-score-item">

                                <div class="bpf-score-item-heading">

                                    <div>

                                        <span class="bpf-score-item-number">
                                            Criterion <?= $index + 1 ?>
                                            · Weight
                                            <?= (float) $criterion['weight_percent'] ?>%
                                        </span>

                                        <label
                                            for="<?= htmlspecialchars(
                                                $inputId,
                                                ENT_QUOTES,
                                                'UTF-8'
                                            ) ?>"
                                            class="bpf-score-item-title"
                                        >
                                            <?= htmlspecialchars(
                                                (string) $criterion['name'],
                                                ENT_QUOTES,
                                                'UTF-8'
                                            ) ?>
                                        </label>

                                    </div>

                                    <div class="bpf-score-input-wrap">

                                        <input
                                            type="number"
                                            id="<?= htmlspecialchars(
                                                $inputId,
                                                ENT_QUOTES,
                                                'UTF-8'
                                            ) ?>"
                                            name="criterion[<?= $criterionId ?>]"
                                            class="form-control bpf-score-input"
                                            min="0"
                                            max="100"
                                            step="1"
                                            inputmode="numeric"
                                            pattern="[0-9]*"
                                            placeholder="0"
                                            value="<?= htmlspecialchars(
                                                $oldValue,
                                                ENT_QUOTES,
                                                'UTF-8'
                                            ) ?>"
                                            data-weight="<?= (float) $criterion['weight_percent'] ?>"
                                            required
                                        >

                                        <span class="bpf-score-unit">
                                            %
                                        </span>

                                    </div>

                                </div>

                                <p class="bpf-score-item-description">
                                    <?= htmlspecialchars(
                                        (string) $criterion['description'],
                                        ENT_QUOTES,
                                        'UTF-8'
                                    ) ?>
                                </p>

                            </div>

                        <?php endforeach; ?>

                    </fieldset>

                    <div class="bpf-form-group bpf-score-comments">

                        <label
                            for="poster-score-comments"
                            class="bpf-form-label"
                        >
                            Additional Comments

                            <span class="bpf-optional-label">
                                Optional
                            </span>
                        </label>

                        <textarea
                            id="poster-score-comments"
                            name="comments"
                            class="form-control bpf-score-textarea"
                            rows="5"
                            maxlength="1000"
                            placeholder="Add comments about the poster presentation..."
                        ><?= htmlspecialchars(
                            $oldComments,
                            ENT_QUOTES,
                            'UTF-8'
                        ) ?></textarea>

                    </div>

                    <div
                        class="bpf-score-summary"
                        aria-live="polite"
                    >

                        <div>

                            <span>
                                Overall Score
                            </span>

                            <small>
                                Weighted poster score
                            </small>

                        </div>

                        <strong id="bpf-overall-score">
                            0%
                        </strong>

                    </div>

                    <button
                        type="submit"
                        class="btn bpf-btn bpf-btn-primary"
                    >

                        Submit Poster Score

                        <i
                            class="bi bi-check-circle"
                            aria-hidden="true"
                        ></i>

                    </button>

                </form>

            <?php endif; ?>

        </div>

    </section>

    <div
        class="modal fade bpf-success-modal"
        id="bpf-score-success-modal"
        tabindex="-1"
        aria-labelledby="bpf-score-success-title"
        aria-hidden="true"
        data-bs-backdrop="static"
        data-bs-keyboard="false"
    >

        <div class="modal-dialog modal-dialog-centered">

            <div class="modal-content">

                <div class="modal-body">

                    <div
                        class="bpf-success-icon"
                        aria-hidden="true"
                    >
                        <i class="bi bi-check-lg"></i>
                    </div>

                    <h2
                        id="bpf-score-success-title"
                        class="bpf-success-title"
                    >
                        Poster Score Submitted
                    </h2>

                    <p class="bpf-success-message">
                        Thank you for submitting your score.
                    </p>

                    <?php if (
                        $submittedOverallScore !== null
                    ): ?>

                        <p class="bpf-success-message">
                            Your weighted overall score was

                            <strong>
                                <?= htmlspecialchars(
                                    number_format(
                                        $submittedOverallScore,
                                        2
                                    ),
                                    ENT_QUOTES,
                                    'UTF-8'
                                ) ?>%
                            </strong>.
                        </p>

                    <?php endif; ?>

                    <p class="bpf-success-question">
                        Would you like to score another poster?
                    </p>

                    <div class="bpf-success-actions">

                        <a
                            href="select_poster_presenter.php"
                            class="btn bpf-btn bpf-btn-primary"
                        >
                            Score Another Poster

                            <i
                                class="bi bi-arrow-right"
                                aria-hidden="true"
                            ></i>
                        </a>

                        <a
                            href="index.php"
                            class="btn bpf-btn-secondary"
                        >
                            Finish
                        </a>

                    </div>

                </div>

            </div>

        </div>

    </div>

</main>

<script src="assets/js/bootstrap.bundle.min.js"></script>
<script src="assets/js/app.js"></script>

<?php if (!$scoreSubmitted): ?>

<script>
    const scoreForm = document.getElementById(
        'bpf-score-form'
    );

    const scoreInputs = document.querySelectorAll(
        '.bpf-score-input'
    );

    const overallScore = document.getElementById(
        'bpf-overall-score'
    );

    function normaliseScore(input) {
        const rawValue = input.value.trim();

        if (rawValue === '') {
            return null;
        }

        let value = Number(rawValue);

        if (!Number.isFinite(value)) {
            input.value = '';
            return null;
        }

        value = Math.round(value);
        value = Math.max(0, Math.min(100, value));

        input.value = String(value);

        return value;
    }

    function updateOverallScore() {
        let weightedTotal = 0;
        let completedWeight = 0;

        scoreInputs.forEach((input) => {
            const rawValue = input.value.trim();

            if (rawValue === '') {
                return;
            }

            const value = Number(rawValue);
            const weight = Number(input.dataset.weight);

            if (
                Number.isFinite(value) &&
                Number.isFinite(weight) &&
                value >= 0 &&
                value <= 100
            ) {
                weightedTotal += value * (weight / 100);
                completedWeight += weight;
            }
        });

        if (completedWeight === 0) {
            overallScore.textContent = '0%';
            return;
        }

        const previewScore = Math.round(
            weightedTotal / (completedWeight / 100)
        );

        overallScore.textContent = `${previewScore}%`;
    }

    scoreInputs.forEach((input) => {

        input.addEventListener('input', () => {
            input.value = input.value.replace(/\D/g, '');

            if (
                input.value !== '' &&
                Number(input.value) > 100
            ) {
                input.value = '100';
            }

            input.classList.remove('is-invalid');

            updateOverallScore();
        });

        input.addEventListener('blur', () => {
            normaliseScore(input);
            updateOverallScore();
        });

    });

    scoreForm.addEventListener('submit', (event) => {
        let isValid = true;
        let firstInvalidInput = null;

        scoreInputs.forEach((input) => {
            const value = normaliseScore(input);

            if (
                value === null ||
                value < 0 ||
                value > 100
            ) {
                isValid = false;
                input.classList.add('is-invalid');

                if (firstInvalidInput === null) {
                    firstInvalidInput = input;
                }
            } else {
                input.classList.remove('is-invalid');
            }
        });

        if (!isValid) {
            event.preventDefault();
            firstInvalidInput?.focus();
        }
    });

    updateOverallScore();
</script>

<?php endif; ?>

<?php if ($scoreSubmitted): ?>

<script>
    document.addEventListener('DOMContentLoaded', () => {
        const modalElement = document.getElementById(
            'bpf-score-success-modal'
        );

        if (modalElement === null) {
            return;
        }

        const successModal = new bootstrap.Modal(
            modalElement
        );

        successModal.show();
    });
</script>

<?php endif; ?>

</body>

</html>