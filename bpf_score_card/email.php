<?php
declare(strict_types=1);

session_start();

require_once __DIR__ . '/includes/database.php';

/*
|--------------------------------------------------------------------------
| Redirect authenticated judges
|--------------------------------------------------------------------------
*/

if (
    isset($_SESSION['judge_id'], $_SESSION['judge_email']) &&
    (int) $_SESSION['judge_id'] > 0 &&
    filter_var(
        (string) $_SESSION['judge_email'],
        FILTER_VALIDATE_EMAIL
    ) !== false
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
| Process email submission
|--------------------------------------------------------------------------
*/

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = strtolower(
        trim((string) ($_POST['email'] ?? ''))
    );

    $csrfToken = (string) ($_POST['csrf_token'] ?? '');

    $_SESSION['old_email'] = $email;

    if (
        $csrfToken === '' ||
        !hash_equals(
            (string) $_SESSION['csrf_token'],
            $csrfToken
        )
    ) {
        $_SESSION['error'] =
            'Your session has expired. Please refresh the page and try again.';

        header('Location: email.php');
        exit;
    }

    if ($email === '') {
        $_SESSION['error'] =
            'Please enter your email address.';

        header('Location: email.php');
        exit;
    }

    if (strlen($email) > 255) {
        $_SESSION['error'] =
            'The email address must not exceed 255 characters.';

        header('Location: email.php');
        exit;
    }

    if (filter_var($email, FILTER_VALIDATE_EMAIL) === false) {
        $_SESSION['error'] =
            'Please enter a valid email address.';

        header('Location: email.php');
        exit;
    }

    try {
        $statement = $pdo->prepare(
            'SELECT
                id,
                email
             FROM judges
             WHERE LOWER(email) = :email
             LIMIT 1'
        );

        $statement->execute([
            'email' => $email,
        ]);

        $judge = $statement->fetch(PDO::FETCH_ASSOC);

        if ($judge === false) {
            $_SESSION['error'] =
                'This email address is not registered as a judge. '
                . 'Please contact the forum administrator.';

            header('Location: email.php');
            exit;
        }

        session_regenerate_id(true);

        $_SESSION['judge_id'] = (int) $judge['id'];
        $_SESSION['judge_email'] = (string) $judge['email'];

        unset(
            $_SESSION['error'],
            $_SESSION['old_email'],
            $_SESSION['selected_presentation_type'],

            $_SESSION['selected_subtheme_id'],
            $_SESSION['selected_subtheme_name'],
            $_SESSION['selected_presenter_id'],
            $_SESSION['selected_presenter_name'],
            $_SESSION['selected_presenter_institution'],
            $_SESSION['selected_presentation_title'],

            $_SESSION['selected_poster_subtheme_id'],
            $_SESSION['selected_poster_subtheme_name'],
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
            $_SESSION['old_poster_comments']
        );

        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));

        header('Location: select_presentation_type.php');
        exit;
    } catch (PDOException $exception) {
        error_log(
            'Judge verification failed: '
            . $exception->getMessage()
        );

        $_SESSION['error'] =
            'We could not verify your email at this time. Please try again.';

        header('Location: email.php');
        exit;
    }
}

/*
|--------------------------------------------------------------------------
| Display form
|--------------------------------------------------------------------------
*/

$error = (string) (
    $_SESSION['error'] ?? ''
);

$oldEmail = (string) (
    $_SESSION['old_email'] ?? ''
);

unset(
    $_SESSION['error'],
    $_SESSION['old_email']
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
        content="Enter your email to begin scoring presentations."
    >

    <meta
        name="theme-color"
        content="#06124F"
    >

    <title>
        Judge Email | Best Practices Forum Score Card
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

        $backLink = 'index.php';

        include __DIR__ . '/includes/app_header.php';

        ?>

        <!-- ==========================================================
             PAGE CONTENT
        =========================================================== -->

        <div class="bpf-content">

            <p class="bpf-step-label">
                Step 1 of 4
            </p>

            <h1
                id="bpf-page-title"
                class="bpf-title"
            >
                Enter your email
            </h1>

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
                action="email.php"
                method="post"
                class="bpf-form"
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

                <div class="bpf-form-group">

                    <label
                        for="bpf-email"
                        class="bpf-form-label"
                    >
                        Email Address
                    </label>

                    <div class="bpf-input-group">

                        <i
                            class="bi bi-envelope bpf-input-icon"
                            aria-hidden="true"
                        ></i>

                        <input
                            type="email"
                            id="bpf-email"
                            name="email"
                            class="form-control bpf-input"
                            placeholder="judge@example.com"
                            value="<?= htmlspecialchars(
                                $oldEmail,
                                ENT_QUOTES,
                                'UTF-8'
                            ) ?>"
                            autocomplete="email"
                            inputmode="email"
                            maxlength="255"
                            required
                        >

                    </div>

                </div>

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

        <footer class="bpf-footer">

            Your email is used only for judging and retrieving your submitted scores.

        </footer>

    </section>

</main>

<script src="assets/js/bootstrap.bundle.min.js"></script>
<script src="assets/js/app.js"></script>

</body>

</html>