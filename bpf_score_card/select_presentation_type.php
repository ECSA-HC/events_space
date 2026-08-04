<?php
declare(strict_types=1);

session_start();

/*
|--------------------------------------------------------------------------
| Require judge authentication
|--------------------------------------------------------------------------
*/

if (
    !isset($_SESSION['judge_id'], $_SESSION['judge_email']) ||
    (int) $_SESSION['judge_id'] <= 0 ||
    filter_var(
        (string) $_SESSION['judge_email'],
        FILTER_VALIDATE_EMAIL
    ) === false
) {
    $_SESSION['error'] =
        'Please enter your registered email address before continuing.';

    header('Location: email.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Generate CSRF token
|--------------------------------------------------------------------------
*/

if (
    !isset($_SESSION['csrf_token']) ||
    !is_string($_SESSION['csrf_token']) ||
    $_SESSION['csrf_token'] === ''
) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

/*
|--------------------------------------------------------------------------
| Process presentation-type selection
|--------------------------------------------------------------------------
*/

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $presentationType = strtolower(
        trim((string) ($_POST['presentation_type'] ?? ''))
    );

    $csrfToken = (string) ($_POST['csrf_token'] ?? '');

    if (
        $csrfToken === '' ||
        !hash_equals(
            (string) $_SESSION['csrf_token'],
            $csrfToken
        )
    ) {
        $_SESSION['error'] =
            'Your session has expired. Please try again.';

        header('Location: select_presentation_type.php');
        exit;
    }

    if (!in_array($presentationType, ['oral', 'poster'], true)) {
        $_SESSION['error'] =
            'Please select a valid presentation type.';

        header('Location: select_presentation_type.php');
        exit;
    }

    /*
     * Clear all previous oral and poster scoring state.
     */
    unset(
        $_SESSION['selected_subtheme_id'],
        $_SESSION['selected_subtheme_name'],

        $_SESSION['selected_presenter_id'],
        $_SESSION['selected_presenter_name'],
        $_SESSION['selected_presenter_institution'],
        $_SESSION['selected_presentation_title'],

        $_SESSION['selected_poster_presenter_id'],
        $_SESSION['selected_poster_presenter_name'],
        $_SESSION['selected_poster_presenter_institution'],
        $_SESSION['selected_poster_title'],

        $_SESSION['score_submitted'],
        $_SESSION['poster_score_submitted'],

        $_SESSION['last_overall_score'],
        $_SESSION['last_poster_overall_score'],

        $_SESSION['old_scores'],
        $_SESSION['old_poster_scores'],
        $_SESSION['old_comments'],
        $_SESSION['old_poster_comments'],

        $_SESSION['error']
    );

    $_SESSION['selected_presentation_type'] = $presentationType;
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));

    if ($presentationType === 'poster') {
        header('Location: select_poster_presenter.php');
        exit;
    }

    header('Location: select_subtheme.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Retrieve page values
|--------------------------------------------------------------------------
*/

$error = (string) ($_SESSION['error'] ?? '');

$selectedPresentationType = (
    isset($_SESSION['selected_presentation_type']) &&
    in_array(
        $_SESSION['selected_presentation_type'],
        ['oral', 'poster'],
        true
    )
)
    ? (string) $_SESSION['selected_presentation_type']
    : '';

unset($_SESSION['error']);
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
        content="Select whether you want to score an oral or poster presentation."
    >

    <meta
        name="theme-color"
        content="#06124F"
    >

    <title>
        Select Presentation Type | Best Practices Forum Score Card
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

        $backLink = 'email.php';

        include __DIR__ . '/includes/app_header.php';

        ?>

        <div class="bpf-content">

            <p class="bpf-step-label">
                Step 2 of 3/4
            </p>

            <h1
                id="bpf-page-title"
                class="bpf-title"
            >
                Presentation Type
            </h1>

            <p class="bpf-description">
                Choose whether you want to score an oral or poster
                presentation.
            </p>

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

            <form
                action="select_presentation_type.php"
                method="post"
                class="bpf-form"
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

                <fieldset class="bpf-subtheme-fieldset">

                    <legend class="visually-hidden">
                        Available presentation types
                    </legend>

                    <div class="bpf-subtheme-list">

                        <label class="bpf-subtheme-option">

                            <input
                                type="radio"
                                name="presentation_type"
                                value="oral"
                                class="bpf-subtheme-input"
                                <?= $selectedPresentationType === 'oral'
                                    ? 'checked'
                                    : '' ?>
                                required
                            >

                            <span class="bpf-subtheme-card">

                                <span class="bpf-subtheme-number">
                                    <i
                                        class="bi bi-mic-fill"
                                        aria-hidden="true"
                                    ></i>
                                </span>

                                <span class="bpf-subtheme-text">
                                    <strong>
                                        Oral Presentation
                                    </strong>

                                    <small>
                                        <br>Score a live oral presentation using
                                        the oral presentation criteria.
                                    </small>
                                </span>

                                <span
                                    class="bpf-subtheme-check"
                                    aria-hidden="true"
                                >
                                    <i class="bi bi-check-circle-fill"></i>
                                </span>

                            </span>

                        </label>

                        <label class="bpf-subtheme-option">

                            <input
                                type="radio"
                                name="presentation_type"
                                value="poster"
                                class="bpf-subtheme-input"
                                <?= $selectedPresentationType === 'poster'
                                    ? 'checked'
                                    : '' ?>
                                required
                            >

                            <span class="bpf-subtheme-card">

                                <span class="bpf-subtheme-number">
                                    <i
                                        class="bi bi-easel-fill"
                                        aria-hidden="true"
                                    ></i>
                                </span>

                                <span class="bpf-subtheme-text">
                                    <strong>
                                        Poster Presentation
                                    </strong>

                                    <small>
                                        <br>Score a poster presentation using
                                        the poster-specific criteria.
                                    </small>
                                </span>

                                <span
                                    class="bpf-subtheme-check"
                                    aria-hidden="true"
                                >
                                    <i class="bi bi-check-circle-fill"></i>
                                </span>

                            </span>

                        </label>

                    </div>

                </fieldset>

                <!-- <div
                    class="bpf-info-banner"
                    role="note"
                >

                    <i
                        class="bi bi-info-circle"
                        aria-hidden="true"
                    ></i>

                    <span>
                        Oral and poster presentations use different
                        scoring criteria.
                    </span>

                </div> -->

                <button
                    type="submit"
                    class="btn bpf-btn bpf-btn-primary"
                >

                    Continue

                    <i
                        class="bi bi-arrow-right"
                        aria-hidden="true"
                    ></i>

                </button>

            </form>

        </div>

    </section>

</main>

<script src="assets/js/bootstrap.bundle.min.js"></script>
<script src="assets/js/app.js"></script>

</body>

</html>