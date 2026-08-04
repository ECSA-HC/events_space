<?php
declare(strict_types=1);

session_start();

define('APP_ROOT', dirname(__DIR__));

require_once APP_ROOT . '/includes/database.php';

/*
|--------------------------------------------------------------------------
| Require authenticated administrator
|--------------------------------------------------------------------------
*/

if (($_SESSION['admin_authenticated'] ?? false) !== true) {
    header('Location: login.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Helper functions
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
        !isset($_SESSION['create_admin_csrf']) ||
        !is_string($_SESSION['create_admin_csrf'])
    ) {
        $_SESSION['create_admin_csrf'] = bin2hex(
            random_bytes(32)
        );
    }

    return $_SESSION['create_admin_csrf'];
}

function isValidCsrfToken(string $token): bool
{
    $sessionToken = $_SESSION['create_admin_csrf'] ?? '';

    return is_string($sessionToken)
        && $sessionToken !== ''
        && hash_equals($sessionToken, $token);
}

/*
|--------------------------------------------------------------------------
| Form state
|--------------------------------------------------------------------------
*/

$error = '';
$success = '';
$fullName = '';
$email = '';

/*
|--------------------------------------------------------------------------
| Process administrator creation
|--------------------------------------------------------------------------
*/

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $fullName = trim(
        (string) ($_POST['full_name'] ?? '')
    );

    $email = strtolower(
        trim((string) ($_POST['email'] ?? ''))
    );

    $password = (string) ($_POST['password'] ?? '');

    $confirmPassword = (string) (
        $_POST['confirm_password'] ?? ''
    );

    $csrfToken = (string) (
        $_POST['csrf_token'] ?? ''
    );

    if (!isValidCsrfToken($csrfToken)) {
        $error =
            'The request could not be verified. Please try again.';
    } elseif ($fullName === '') {
        $error = 'Enter the administrator name.';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $error =
            'Enter a valid administrator email address.';
    } elseif (strlen($password) < 12) {
        $error =
            'The password must contain at least 12 characters.';
    } elseif ($password !== $confirmPassword) {
        $error =
            'The password confirmation does not match.';
    } else {
        $statement = $pdo->prepare(
            '
                INSERT INTO administrators (
                    full_name,
                    email,
                    password_hash,
                    is_active
                )
                VALUES (
                    :full_name,
                    :email,
                    :password_hash,
                    1
                )
            '
        );

        try {
            $statement->execute([
                'full_name' => $fullName,
                'email' => $email,
                'password_hash' => password_hash(
                    $password,
                    PASSWORD_DEFAULT
                ),
            ]);

            $success =
                'Administrator account created successfully.';

            $fullName = '';
            $email = '';

            /*
            |--------------------------------------------------------------------------
            | Regenerate the CSRF token after successful submission
            |--------------------------------------------------------------------------
            */

            unset($_SESSION['create_admin_csrf']);
        } catch (PDOException $exception) {
            if ((string) $exception->getCode() === '23000') {
                $error =
                    'An administrator with that email address already exists.';
            } else {
                throw $exception;
            }
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

    <title>Add Administrator | Score Card</title>

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

<body class="setup-page">

<main class="setup-container">

    <section class="setup-card">

        <div class="setup-card__header">

            <div>
                <p class="admin-login__card-label">
                    Administrator management
                </p>

                <h1>Add administrator</h1>
            </div>

            <a
                href="index.php"
                class="setup-card__back-link"
            >
                <i
                    class="bi bi-arrow-left"
                    aria-hidden="true"
                ></i>

                Back to dashboard
            </a>

        </div>

        <p>
            Create an additional administrator account for the
            Score Card dashboard.
        </p>

        <?php if ($error !== ''): ?>

            <div
                class="admin-login__alert"
                role="alert"
            >
                <i
                    class="bi bi-exclamation-circle-fill"
                    aria-hidden="true"
                ></i>

                <span><?= escape($error) ?></span>
            </div>

        <?php endif; ?>

        <?php if ($success !== ''): ?>

            <div
                class="setup-success"
                role="status"
            >
                <i
                    class="bi bi-check-circle-fill"
                    aria-hidden="true"
                ></i>

                <span><?= escape($success) ?></span>
            </div>

        <?php endif; ?>

        <form
            method="post"
            action="create_admin.php"
        >

            <input
                type="hidden"
                name="csrf_token"
                value="<?= escape($csrfToken) ?>"
            >

            <div class="admin-login__field">

                <label for="full_name">
                    Full name
                </label>

                <input
                    type="text"
                    id="full_name"
                    name="full_name"
                    value="<?= escape($fullName) ?>"
                    maxlength="150"
                    autocomplete="name"
                    required
                >

            </div>

            <div class="admin-login__field">

                <label for="email">
                    Email address
                </label>

                <input
                    type="email"
                    id="email"
                    name="email"
                    value="<?= escape($email) ?>"
                    maxlength="190"
                    autocomplete="email"
                    required
                >

            </div>

            <div class="admin-login__field">

                <label for="password">
                    Password
                </label>

                <input
                    type="password"
                    id="password"
                    name="password"
                    minlength="12"
                    autocomplete="new-password"
                    required
                >

                <small>
                    Use at least 12 characters.
                </small>

            </div>

            <div class="admin-login__field">

                <label for="confirm_password">
                    Confirm password
                </label>

                <input
                    type="password"
                    id="confirm_password"
                    name="confirm_password"
                    minlength="12"
                    autocomplete="new-password"
                    required
                >

            </div>

            <button
                type="submit"
                class="admin-login__submit"
            >
                <i
                    class="bi bi-person-plus-fill"
                    aria-hidden="true"
                ></i>

                Create administrator
            </button>

        </form>

    </section>

</main>

</body>
</html>