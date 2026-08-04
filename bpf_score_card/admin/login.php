<?php
declare(strict_types=1);

session_start();

define('APP_ROOT', dirname(__DIR__));

require_once APP_ROOT . '/includes/database.php';

/*
|--------------------------------------------------------------------------
| Already authenticated
|--------------------------------------------------------------------------
*/

if (($_SESSION['admin_authenticated'] ?? false) === true) {
    header('Location: index.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Security helpers
|--------------------------------------------------------------------------
*/

function escape(?string $value): string
{
    return htmlspecialchars(
        $value ?? '',
        ENT_QUOTES,
        'UTF-8'
    );
}

function generateCsrfToken(): string
{
    if (
        !isset($_SESSION['admin_login_csrf']) ||
        !is_string($_SESSION['admin_login_csrf'])
    ) {
        $_SESSION['admin_login_csrf'] = bin2hex(random_bytes(32));
    }

    return $_SESSION['admin_login_csrf'];
}

function isValidCsrfToken(string $token): bool
{
    $sessionToken = $_SESSION['admin_login_csrf'] ?? '';

    return is_string($sessionToken)
        && $sessionToken !== ''
        && hash_equals($sessionToken, $token);
}

/*
|--------------------------------------------------------------------------
| Login attempt throttling
|--------------------------------------------------------------------------
|
| This is session-based throttling. It slows repeated attempts from the same
| browser session. Server-level rate limiting may be added later if required.
|
*/

function registerFailedAttempt(): void
{
    $attempts = (int) ($_SESSION['admin_login_attempts'] ?? 0);

    $_SESSION['admin_login_attempts'] = $attempts + 1;
    $_SESSION['admin_last_failed_login'] = time();
}

function clearFailedAttempts(): void
{
    unset(
        $_SESSION['admin_login_attempts'],
        $_SESSION['admin_last_failed_login']
    );
}

function remainingLockSeconds(): int
{
    $attempts = (int) ($_SESSION['admin_login_attempts'] ?? 0);
    $lastAttempt = (int) ($_SESSION['admin_last_failed_login'] ?? 0);

    if ($attempts < 5 || $lastAttempt < 1) {
        return 0;
    }

    $lockDuration = 300;
    $remaining = $lockDuration - (time() - $lastAttempt);

    if ($remaining <= 0) {
        clearFailedAttempts();

        return 0;
    }

    return $remaining;
}

/*
|--------------------------------------------------------------------------
| Process login
|--------------------------------------------------------------------------
*/

$error = '';
$email = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = strtolower(trim((string) ($_POST['email'] ?? '')));
    $password = (string) ($_POST['password'] ?? '');
    $csrfToken = (string) ($_POST['csrf_token'] ?? '');

    $remainingSeconds = remainingLockSeconds();

    if ($remainingSeconds > 0) {
        $minutes = (int) ceil($remainingSeconds / 60);

        $error = sprintf(
            'Too many unsuccessful login attempts. Try again in %d %s.',
            $minutes,
            $minutes === 1 ? 'minute' : 'minutes'
        );
    } elseif (!isValidCsrfToken($csrfToken)) {
        $error = 'The login request could not be verified. Please try again.';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $error = 'Enter a valid administrator email address.';
    } elseif ($password === '') {
        $error = 'Enter your password.';
    } else {
        $statement = $pdo->prepare(
            '
                SELECT
                    id,
                    full_name,
                    email,
                    password_hash,
                    is_active
                FROM administrators
                WHERE email = :email
                LIMIT 1
            '
        );

        $statement->execute([
            'email' => $email,
        ]);

        $administrator = $statement->fetch(PDO::FETCH_ASSOC);

        $validLogin =
            is_array($administrator)
            && (int) $administrator['is_active'] === 1
            && password_verify(
                $password,
                (string) $administrator['password_hash']
            );

        if (!$validLogin) {
            registerFailedAttempt();

            $error = 'The email address or password is incorrect.';
        } else {
            clearFailedAttempts();

            if (
                password_needs_rehash(
                    (string) $administrator['password_hash'],
                    PASSWORD_DEFAULT
                )
            ) {
                $newPasswordHash = password_hash(
                    $password,
                    PASSWORD_DEFAULT
                );

                $rehashStatement = $pdo->prepare(
                    '
                        UPDATE administrators
                        SET password_hash = :password_hash
                        WHERE id = :id
                    '
                );

                $rehashStatement->execute([
                    'password_hash' => $newPasswordHash,
                    'id' => (int) $administrator['id'],
                ]);
            }

            $updateLoginStatement = $pdo->prepare(
                '
                    UPDATE administrators
                    SET last_login_at = CURRENT_TIMESTAMP
                    WHERE id = :id
                '
            );

            $updateLoginStatement->execute([
                'id' => (int) $administrator['id'],
            ]);

            session_regenerate_id(true);

            $_SESSION['admin_authenticated'] = true;
            $_SESSION['admin_id'] = (int) $administrator['id'];
            $_SESSION['admin_name'] =
                (string) $administrator['full_name'];
            $_SESSION['admin_email'] =
                (string) $administrator['email'];
            $_SESSION['admin_logged_in_at'] = time();

            unset($_SESSION['admin_login_csrf']);

            header('Location: index.php');
            exit;
        }
    }
}

$csrfToken = generateCsrfToken();
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Admin Login | Score Card</title>

    <link
        rel="icon"
        type="image/png"
        href="../assets/images/favicon.png"
    >

    <link
        rel="stylesheet"
        href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css"
    >

    <link
        rel="stylesheet"
        href="assets/css/admin_login.css"
    >
</head>

<body>

<main class="admin-login">

    <section class="admin-login__brand-panel">

        <div class="admin-login__brand-content">

            <img
                src="../assets/images/ecsa-logo.png"
                alt="ECSA Health Community logo"
                class="admin-login__logo"
            >

            <p class="admin-login__eyebrow">
                Score Card Administration
            </p>

            <h1 class="admin-login__brand-title">
                Presentation results dashboard
            </h1>

            <p class="admin-login__brand-description">
                Sign in to review oral and poster presentation rankings,
                judge counts and average final scores.
            </p>

            <div class="admin-login__feature-list">

                <span>
                    <i class="bi bi-bar-chart-fill" aria-hidden="true"></i>
                    Consolidated rankings
                </span>

                <span>
                    <i class="bi bi-people-fill" aria-hidden="true"></i>
                    Multi-judge averages
                </span>

                <span>
                    <i class="bi bi-shield-lock-fill" aria-hidden="true"></i>
                    Restricted administrative access
                </span>

            </div>

        </div>

    </section>

    <section class="admin-login__form-panel">

        <div class="admin-login__card">

            <div class="admin-login__card-header">

                <div class="admin-login__lock-icon">
                    <i class="bi bi-shield-lock-fill" aria-hidden="true"></i>
                </div>

                <div>
                    <p class="admin-login__card-label">
                        Administrator access
                    </p>

                    <h2 class="admin-login__card-title">
                        Sign in
                    </h2>
                </div>

            </div>

            <p class="admin-login__instruction">
                Enter your registered administrator credentials.
            </p>

            <?php if ($error !== ''): ?>

                <div class="admin-login__alert" role="alert">
                    <i
                        class="bi bi-exclamation-circle-fill"
                        aria-hidden="true"
                    ></i>

                    <span><?= escape($error) ?></span>
                </div>

            <?php endif; ?>

            <form method="post" action="login.php" class="admin-login__form">

                <input
                    type="hidden"
                    name="csrf_token"
                    value="<?= escape($csrfToken) ?>"
                >

                <div class="admin-login__field">

                    <label for="email">
                        Email address
                    </label>

                    <div class="admin-login__input-wrapper">

                        <i
                            class="bi bi-envelope-fill"
                            aria-hidden="true"
                        ></i>

                        <input
                            type="email"
                            id="email"
                            name="email"
                            value="<?= escape($email) ?>"
                            autocomplete="username"
                            inputmode="email"
                            maxlength="190"
                            required
                            autofocus
                        >

                    </div>

                </div>

                <div class="admin-login__field">

                    <label for="password">
                        Password
                    </label>

                    <div class="admin-login__input-wrapper">

                        <i
                            class="bi bi-key-fill"
                            aria-hidden="true"
                        ></i>

                        <input
                            type="password"
                            id="password"
                            name="password"
                            autocomplete="current-password"
                            required
                        >

                        <button
                            type="button"
                            class="admin-login__password-toggle"
                            id="password-toggle"
                            aria-label="Show password"
                            aria-pressed="false"
                        >
                            <i
                                class="bi bi-eye-fill"
                                aria-hidden="true"
                            ></i>
                        </button>

                    </div>

                </div>

                <button
                    type="submit"
                    class="admin-login__submit"
                >
                    <i
                        class="bi bi-box-arrow-in-right"
                        aria-hidden="true"
                    ></i>

                    Sign in to dashboard
                </button>

            </form>

            <p class="admin-login__security-note">
                <i class="bi bi-lock-fill" aria-hidden="true"></i>
                Access is restricted to authorised administrators.
            </p>

        </div>

    </section>

</main>

<script>
'use strict';

const passwordInput = document.getElementById('password');
const passwordToggle = document.getElementById('password-toggle');

passwordToggle.addEventListener('click', () => {
    const passwordVisible = passwordInput.type === 'text';

    passwordInput.type = passwordVisible ? 'password' : 'text';
    passwordToggle.setAttribute(
        'aria-label',
        passwordVisible ? 'Show password' : 'Hide password'
    );
    passwordToggle.setAttribute(
        'aria-pressed',
        passwordVisible ? 'false' : 'true'
    );

    const icon = passwordToggle.querySelector('i');

    icon.className = passwordVisible
        ? 'bi bi-eye-fill'
        : 'bi bi-eye-slash-fill';
});
</script>

</body>
</html>
