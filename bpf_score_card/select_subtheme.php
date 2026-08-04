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
| Require oral presentation flow
|--------------------------------------------------------------------------
*/

if (
    ($_SESSION['selected_presentation_type'] ?? '') !== 'oral'
) {
    header('Location: select_presentation_type.php');
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
| Process sub-theme selection
|--------------------------------------------------------------------------
*/

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $submittedSubthemeId = filter_input(
        INPUT_POST,
        'subtheme',
        FILTER_VALIDATE_INT
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

        header('Location: select_subtheme.php');
        exit;
    }

    if (
        $submittedSubthemeId === false ||
        $submittedSubthemeId === null ||
        $submittedSubthemeId < 1
    ) {
        $_SESSION['error'] =
            'Please select a valid sub-theme.';

        header('Location: select_subtheme.php');
        exit;
    }

    try {
        $statement = $pdo->prepare(
            'SELECT id, name
             FROM subthemes
             WHERE id = :id
               AND is_active = 1
             LIMIT 1'
        );

        $statement->execute([
            'id' => $submittedSubthemeId,
        ]);

        $subtheme = $statement->fetch(PDO::FETCH_ASSOC);

        if ($subtheme === false) {
            $_SESSION['error'] =
                'The selected sub-theme is not available.';

            header('Location: select_subtheme.php');
            exit;
        }

        $_SESSION['selected_subtheme_id'] =
            (int) $subtheme['id'];

        $_SESSION['selected_subtheme_name'] =
            (string) $subtheme['name'];

        unset(
            $_SESSION['selected_presenter_id'],
            $_SESSION['selected_presenter_name'],
            $_SESSION['selected_presenter_institution'],
            $_SESSION['selected_presentation_title'],
            $_SESSION['score_submitted'],
            $_SESSION['last_overall_score'],
            $_SESSION['old_scores'],
            $_SESSION['old_comments'],
            $_SESSION['error']
        );

        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));

        header('Location: select_presenter.php');
        exit;
    } catch (PDOException $exception) {
        error_log(
            'Sub-theme selection failed: '
            . $exception->getMessage()
        );

        $_SESSION['error'] =
            'We could not process your selection. Please try again.';

        header('Location: select_subtheme.php');
        exit;
    }
}

/*
|--------------------------------------------------------------------------
| Retrieve active sub-themes
|--------------------------------------------------------------------------
*/

try {
    $statement = $pdo->query(
        'SELECT id, name
         FROM subthemes
         WHERE is_active = 1
         ORDER BY display_order ASC, id ASC'
    );

    $subthemes = $statement->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $exception) {
    error_log(
        'Sub-theme retrieval failed: '
        . $exception->getMessage()
    );

    $subthemes = [];

    $_SESSION['error'] =
        'Sub-themes could not be loaded at this time.';
}

/*
|--------------------------------------------------------------------------
| Retrieve flash and previous-selection values
|--------------------------------------------------------------------------
*/

$error = (string) ($_SESSION['error'] ?? '');

$selectedSubthemeId = (int) (
    $_SESSION['selected_subtheme_id'] ?? 0
);

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
        content="Select the sub-theme containing the presentation you want to score."
    >

    <meta
        name="theme-color"
        content="#06124F"
    >

    <title>
        Select Sub-theme | Best Practices Forum Score Card
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

        <!-- ==========================================================
             APPLICATION HEADER
        =========================================================== -->

        <?php

        $backLink = 'email.php';

        include __DIR__ . '/includes/app_header.php';

        ?>

        <!-- ==========================================================
             PAGE CONTENT
        =========================================================== -->

        <div class="bpf-content bpf-subtheme-content">

            <p class="bpf-step-label">
                Step 3 of 4
            </p>

            <h1
                id="bpf-page-title"
                class="bpf-title"
            >
                Select Sub-theme
            </h1>

            <p class="bpf-description">
                Choose the sub-theme containing the presentation you want
                to score.
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

            <?php if ($subthemes !== []): ?>

                <form
                    action="select_subtheme.php"
                    method="post"
                    class="bpf-form"
                    id="bpf-subtheme-form"
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
                            Available sub-themes
                        </legend>

                        <div class="bpf-subtheme-list">

                            <?php foreach ($subthemes as $index => $subtheme): ?>

                                <?php
                                $subthemeId = (int) $subtheme['id'];
                                $subthemeName = (string) $subtheme['name'];

                                /*
                                 * Restore the judge's previous selection.
                                 * When no previous selection exists, select
                                 * the first available sub-theme.
                                 */
                                $isChecked =
                                    $selectedSubthemeId > 0
                                        ? $selectedSubthemeId === $subthemeId
                                        : $index === 0;
                                ?>

                                <label class="bpf-subtheme-option">

                                    <input
                                        type="radio"
                                        name="subtheme"
                                        value="<?= $subthemeId ?>"
                                        class="bpf-subtheme-input"
                                        <?= $isChecked ? 'checked' : '' ?>
                                        required
                                    >

                                    <span class="bpf-subtheme-card">

                                        <span class="bpf-subtheme-number">
                                            <?= $subthemeId ?>
                                        </span>

                                        <span class="bpf-subtheme-text">
                                            <?= htmlspecialchars(
                                                $subthemeName,
                                                ENT_QUOTES,
                                                'UTF-8'
                                            ) ?>
                                        </span>

                                        <span
                                            class="bpf-subtheme-check"
                                            aria-hidden="true"
                                        >
                                            <i class="bi bi-check-circle-fill"></i>
                                        </span>

                                    </span>

                                </label>

                            <?php endforeach; ?>

                        </div>

                    </fieldset>

                    <div
                        class="bpf-info-banner"
                        role="note"
                    >

                        <i
                            class="bi bi-info-circle"
                            aria-hidden="true"
                        ></i>

                        <span>
                            You can score presentations from one sub-theme
                            at a time.
                        </span>

                    </div>

                    <button
                        type="submit"
                        class="btn bpf-btn bpf-btn-primary"
                    >

                        Next

                        <i
                            class="bi bi-arrow-right"
                            aria-hidden="true"
                        ></i>

                    </button>

                </form>

            <?php else: ?>

                <div
                    class="alert alert-warning bpf-alert"
                    role="alert"
                >
                    No sub-themes are currently available. Please contact
                    the forum administrator.
                </div>

            <?php endif; ?>

        </div>

    </section>

</main>

<script src="assets/js/bootstrap.bundle.min.js"></script>
<script src="assets/js/app.js"></script>

</body>

</html>