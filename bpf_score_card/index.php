<?php
declare(strict_types=1);

session_start();

if (
    isset($_SESSION['judge_id'], $_SESSION['judge_email']) &&
    (int) $_SESSION['judge_id'] > 0 &&
    filter_var($_SESSION['judge_email'], FILTER_VALIDATE_EMAIL)
) {
    header('Location: select_presentation_type.php');
    exit;
}
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
        content="Best Practices Forum presentation judging score card."
    >

    <meta name="theme-color" content="#06124F">

    <title>Best Practices Forum Score Card</title>

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
        href="assets/css/bootstrap-icons.min.css"
    >

    <link
        rel="stylesheet"
        href="assets/css/app.css"
    >
</head>

<body>

<main class="bpf-welcome-page">

    <section
        class="bpf-welcome-card"
        aria-labelledby="bpf-page-title"
    >

        <div class="bpf-welcome-content">

            <div class="bpf-logo-container">
                <img
                    src="assets/images/ecsa-logo.png"
                    alt="East, Central and Southern Africa Health Community logo"
                >
            </div>

            <h1
                id="bpf-page-title"
                class="bpf-forum-title"
            >
                Best Practices Forum
            </h1>

            <p class="bpf-score-card-title">
                Score Card
            </p>

            <div
                class="bpf-title-divider"
                aria-hidden="true"
            ></div>

            <h2 class="bpf-welcome-heading">
                Welcome, Judge!
            </h2>

            <p class="bpf-welcome-message">
                Thank you for helping us recognise and celebrate impactful
                health innovations across the East, Central and Southern
                Africa region.
            </p>

            <div class="bpf-action-buttons">

                <a
                    href="email.php"
                    class="btn bpf-btn bpf-btn-start"
                >
                    <i
                        class="bi bi-arrow-right-circle-fill"
                        aria-hidden="true"
                    ></i>

                    <span>Get Started</span>
                </a>

            </div>

        </div>

        <div
            class="bpf-background-decoration"
            aria-hidden="true"
        ></div>

    </section>

</main>

<script src="assets/js/bootstrap.bundle.min.js"></script>
<script src="assets/js/app.js"></script>

</body>
</html>