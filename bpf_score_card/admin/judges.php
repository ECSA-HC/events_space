<?php
declare(strict_types=1);

session_start();

define('APP_ROOT', dirname(__DIR__));

require_once APP_ROOT . '/includes/database.php';

/*
|--------------------------------------------------------------------------
| Require administrator authentication
|--------------------------------------------------------------------------
*/

if (($_SESSION['admin_authenticated'] ?? false) !== true) {
    header('Location: login.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Escape output
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

/*
|--------------------------------------------------------------------------
| CSRF token
|--------------------------------------------------------------------------
*/

if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

$email = '';
$error = '';
$success = '';

/*
|--------------------------------------------------------------------------
| Process judge management actions
|--------------------------------------------------------------------------
*/

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $submittedToken =
        (string) ($_POST['csrf_token'] ?? '');

    $action = (string) ($_POST['action'] ?? 'add');

    if (
        !hash_equals(
            (string) $_SESSION['csrf_token'],
            $submittedToken
        )
    ) {
        $error =
            'The request could not be verified. Please refresh the page and try again.';
    } elseif ($action === 'delete') {
        $judgeId = filter_input(
            INPUT_POST,
            'judge_id',
            FILTER_VALIDATE_INT,
            [
                'options' => [
                    'min_range' => 1,
                ],
            ]
        );

        if ($judgeId === false || $judgeId === null) {
            $error = 'The selected judge is invalid.';
        } else {
            try {
                $judgeLookupStatement = $pdo->prepare(
                    'SELECT email
                     FROM judges
                     WHERE id = :id
                     LIMIT 1'
                );

                $judgeLookupStatement->execute([
                    'id' => $judgeId,
                ]);

                $judgeEmail = $judgeLookupStatement->fetchColumn();

                if ($judgeEmail === false) {
                    $error = 'The selected judge could not be found.';
                } else {
                    $deleteStatement = $pdo->prepare(
                        'DELETE FROM judges
                         WHERE id = :id'
                    );

                    $deleteStatement->execute([
                        'id' => $judgeId,
                    ]);

                    $success = sprintf(
                        'Judge %s was deleted successfully.',
                        (string) $judgeEmail
                    );
                }
            } catch (PDOException $exception) {
                error_log(
                    'Judge deletion failed: ' .
                    $exception->getMessage()
                );

                $error =
                    'The judge could not be deleted. They may already have submitted scores.';
            }
        }
    } elseif ($action === 'add') {
        $email = strtolower(
            trim((string) ($_POST['email'] ?? ''))
        );

        if ($email === '') {
            $error = 'Please enter the judge’s email address.';
        } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            $error = 'Please enter a valid email address.';
        } elseif (strlen($email) > 255) {
            $error = 'The email address is too long.';
        } else {
            $existingStatement = $pdo->prepare(
                'SELECT id
                 FROM judges
                 WHERE LOWER(email) = :email
                 LIMIT 1'
            );

            $existingStatement->execute([
                'email' => $email,
            ]);

            if ($existingStatement->fetchColumn()) {
                $error =
                    'A judge with this email address already exists.';
            } else {
                try {
                    $insertStatement = $pdo->prepare(
                        'INSERT INTO judges (email)
                         VALUES (:email)'
                    );

                    $insertStatement->execute([
                        'email' => $email,
                    ]);

                    $success =
                        'The judge was added successfully.';

                    $email = '';
                } catch (PDOException $exception) {
                    error_log(
                        'Judge creation failed: ' .
                        $exception->getMessage()
                    );

                    $error =
                        'The judge could not be added. Please try again.';
                }
            }
        }
    } else {
        $error = 'The requested judge action is invalid.';
    }
}

/*
|--------------------------------------------------------------------------
| Retrieve judges
|--------------------------------------------------------------------------
*/

$judgeStatement = $pdo->query(
    'SELECT *
     FROM judges
     ORDER BY email ASC'
);

$judges = $judgeStatement->fetchAll(PDO::FETCH_ASSOC);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1"
    >

    <title>Judges | Admin Dashboard</title>

    <link rel="icon" href="../assets/favicon/favicon.ico" sizes="any">
    <link rel="icon" type="image/png" sizes="32x32" href="../assets/favicon/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="../assets/favicon/favicon-16x16.png">
    <link rel="apple-touch-icon" href="../assets/favicon/apple-touch-icon.png">
    <link rel="manifest" href="../assets/favicon/site.webmanifest">
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
        href="assets/css/admin_dashboard.css"
    >
        <link
    rel="stylesheet"
    href="assets/css/admin_management.css"
>
</head>

<body>

<div class="admin-shell">

    <aside class="admin-sidebar">

        <div class="admin-sidebar__brand">

            <img
                src="../assets/images/ecsa-logo.png"
                alt="ECSA Health Community logo"
                class="admin-sidebar__logo"
            >

            <div>
                <p class="admin-sidebar__eyebrow">
                    Score Card
                </p>

                <h1 class="admin-sidebar__title">
                    Administration
                </h1>
            </div>

        </div>

        <nav
            class="admin-sidebar__navigation"
            aria-label="Administrator navigation"
        >

            <a href="index.php" class="admin-sidebar__link">
                <i class="bi bi-speedometer2" aria-hidden="true"></i>
                <span>Dashboard</span>
            </a>

            <a href="scores.php" class="admin-sidebar__link">
                <i class="bi bi-clipboard-data-fill" aria-hidden="true"></i>
                <span>Manage scores</span>
            </a>

            <a href="judges.php" class="admin-sidebar__link admin-sidebar__link--active">
                <i class="bi bi-people-fill" aria-hidden="true"></i>
                <span>Manage judges</span>
            </a>

            <a href="create_admin.php" class="admin-sidebar__link">
                <i class="bi bi-person-plus-fill" aria-hidden="true"></i>
                <span>Add administrator</span>
            </a>

        </nav>

        <div class="admin-sidebar__footer">

            <div class="admin-sidebar__account">

                <div class="admin-sidebar__avatar">
                    <?= escape(
                        strtoupper(
                            substr(
                                (string) ($_SESSION['admin_name'] ?? 'A'),
                                0,
                                1
                            )
                        )
                    ) ?>
                </div>

                <div class="admin-sidebar__account-details">
                    <strong>
                        <?= escape(
                            (string) ($_SESSION['admin_name'] ?? 'Administrator')
                        ) ?>
                    </strong>

                    <span>
                        <?= escape(
                            (string) ($_SESSION['admin_email'] ?? '')
                        ) ?>
                    </span>
                </div>

            </div>

            <a href="logout.php" class="admin-sidebar__logout">
                <i class="bi bi-box-arrow-right" aria-hidden="true"></i>
                <span>Log out</span>
            </a>

        </div>

    </aside>

    <div class="admin-content">

    <main class="admin-main">

        <header class="admin-page-header">
            <div>
                <p class="admin-page-eyebrow">
                    Judge management
                </p>

                <h1>Judges</h1>

                <p>
                    Add authorised judges who can access the scoring
                    application.
                </p>
            </div>

            <div class="admin-header-stat">
                <span>Total judges</span>
                <strong><?= count($judges) ?></strong>
            </div>
        </header>

        <?php if ($success !== ''): ?>
            <div
                class="admin-alert admin-alert-success"
                role="alert"
            >
                <?= escape($success) ?>
            </div>
        <?php endif; ?>

        <?php if ($error !== ''): ?>
            <div
                class="admin-alert admin-alert-error"
                role="alert"
            >
                <?= escape($error) ?>
            </div>
        <?php endif; ?>

        <div class="admin-content-grid">

            <section class="admin-card">
                <div class="admin-card-header">
                    <div>
                        <h2>Add Judge</h2>

                        <p>
                            Enter the email address the judge will use
                            when accessing the application.
                        </p>
                    </div>
                </div>

                <form
                    method="post"
                    action="judges.php"
                    class="admin-form"
                >
                    <input
                        type="hidden"
                        name="csrf_token"
                        value="<?= escape(
                            (string) $_SESSION['csrf_token']
                        ) ?>"
                    >

                    <input
                        type="hidden"
                        name="action"
                        value="add"
                    >

                    <div class="admin-form-group">
                        <label for="email">
                            Judge email address
                        </label>

                        <input
                            type="email"
                            id="email"
                            name="email"
                            value="<?= escape($email) ?>"
                            maxlength="255"
                            autocomplete="email"
                            placeholder="judge@example.org"
                            required
                        >
                    </div>

                    <button
                        type="submit"
                        class="admin-button admin-button-primary"
                    >
                        <i
                            class="bi bi-person-plus"
                            aria-hidden="true"
                        ></i>

                        Add Judge
                    </button>
                </form>
            </section>

            <section class="admin-card">
                <div class="admin-card-header">
                    <div>
                        <h2>Registered Judges</h2>

                        <p>
                            These email addresses are authorised to
                            participate in scoring.
                        </p>
                    </div>
                </div>

                <?php if ($judges === []): ?>

                    <div class="admin-empty-state">
                        <i
                            class="bi bi-people"
                            aria-hidden="true"
                        ></i>

                        <h3>No judges registered</h3>

                        <p>
                            Add the first judge using the form.
                        </p>
                    </div>

                <?php else: ?>

                    <div class="admin-table-wrapper">
                        <table class="admin-table">
                            <thead>
                            <tr>
                                <th scope="col">ID</th>
                                <th scope="col">Email address</th>

                                <?php if (
                                    array_key_exists(
                                        'created_at',
                                        $judges[0]
                                    )
                                ): ?>
                                    <th scope="col">Added</th>
                                <?php endif; ?>

                                <th scope="col">Action</th>
                            </tr>
                            </thead>

                            <tbody>
                            <?php foreach ($judges as $judge): ?>
                                <tr>
                                    <td>
                                        <?= (int) $judge['id'] ?>
                                    </td>

                                    <td>
                                        <?= escape(
                                            (string) $judge['email']
                                        ) ?>
                                    </td>

                                    <?php if (
                                        array_key_exists(
                                            'created_at',
                                            $judge
                                        )
                                    ): ?>
                                        <td>
                                            <?= escape(
                                                (string) $judge['created_at']
                                            ) ?>
                                        </td>
                                    <?php endif; ?>

                                    <td>
                                        <form
                                            method="post"
                                            action="judges.php"
                                            onsubmit="return confirm('Delete this judge? This action cannot be undone.');"
                                        >
                                            <input
                                                type="hidden"
                                                name="csrf_token"
                                                value="<?= escape(
                                                    (string) $_SESSION['csrf_token']
                                                ) ?>"
                                            >

                                            <input
                                                type="hidden"
                                                name="action"
                                                value="delete"
                                            >

                                            <input
                                                type="hidden"
                                                name="judge_id"
                                                value="<?= (int) $judge['id'] ?>"
                                            >

                                            <button
                                                type="submit"
                                                class="admin-button admin-button-danger admin-button-small"
                                                aria-label="Delete judge <?= escape(
                                                    (string) $judge['email']
                                                ) ?>"
                                            >
                                                <i
                                                    class="bi bi-trash3"
                                                    aria-hidden="true"
                                                ></i>
                                                Delete
                                            </button>
                                        </form>
                                    </td>
                                </tr>
                            <?php endforeach; ?>
                            </tbody>
                        </table>
                    </div>

                <?php endif; ?>

            </section>

        </div>

    </main>

    </div>

</div>

</body>
</html>