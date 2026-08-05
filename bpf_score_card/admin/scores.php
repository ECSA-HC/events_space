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

function escape(mixed $value): string
{
    if ($value === null) {
        return '';
    }

    return htmlspecialchars(
        (string) $value,
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

/*
|--------------------------------------------------------------------------
| Delete score
|--------------------------------------------------------------------------
*/

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $submittedToken =
        (string) ($_POST['csrf_token'] ?? '');

    if (
        !hash_equals(
            (string) $_SESSION['csrf_token'],
            $submittedToken
        )
    ) {
        $_SESSION['error'] =
            'The request could not be verified. Please try again.';

        header('Location: scores.php');
        exit;
    }

    $scoreId = filter_input(
        INPUT_POST,
        'score_id',
        FILTER_VALIDATE_INT
    );

    if (!$scoreId || $scoreId < 1) {
        $_SESSION['error'] = 'Invalid score selected.';

        header('Location: scores.php');
        exit;
    }

    try {
        $pdo->beginTransaction();

        /*
         * Child score-item records should be removed automatically
         * where their foreign keys use ON DELETE CASCADE.
         */
        $deleteStatement = $pdo->prepare(
            'DELETE FROM scores WHERE id = :score_id'
        );

        $deleteStatement->execute([
            'score_id' => $scoreId,
        ]);

        if ($deleteStatement->rowCount() < 1) {
            throw new RuntimeException(
                'The selected score could not be found.'
            );
        }

        $pdo->commit();

        $_SESSION['success'] =
            'The score and its associated score items were deleted.';
    } catch (Throwable $exception) {
        if ($pdo->inTransaction()) {
            $pdo->rollBack();
        }

        error_log(
            'Score deletion failed: ' . $exception->getMessage()
        );

        $_SESSION['error'] =
            'The score could not be deleted. Please check whether its related score-item records use ON DELETE CASCADE.';
    }

    header('Location: scores.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Retrieve score table columns
|--------------------------------------------------------------------------
*/

$columnStatement = $pdo->query(
    'SHOW COLUMNS FROM scores'
);

$columns = $columnStatement->fetchAll(PDO::FETCH_ASSOC);

$columnNames = array_map(
    static fn(array $column): string =>
        (string) $column['Field'],
    $columns
);

/*
|--------------------------------------------------------------------------
| Retrieve all scores
|--------------------------------------------------------------------------
*/

$orderColumn = in_array('created_at', $columnNames, true)
    ? 'created_at'
    : 'id';

$scoreStatement = $pdo->query(
    sprintf(
        'SELECT * FROM scores ORDER BY `%s` DESC',
        $orderColumn
    )
);

$scores = $scoreStatement->fetchAll(PDO::FETCH_ASSOC);

$success = (string) ($_SESSION['success'] ?? '');
$error = (string) ($_SESSION['error'] ?? '');

unset(
    $_SESSION['success'],
    $_SESSION['error']
);
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1"
    >

    <title>Scores | Admin Dashboard</title>

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

            <a href="scores.php" class="admin-sidebar__link admin-sidebar__link--active">
                <i class="bi bi-clipboard-data-fill" aria-hidden="true"></i>
                <span>Manage scores</span>
            </a>

            <a href="judges.php" class="admin-sidebar__link">
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
                    Score management
                </p>

                <h1>Submitted Scores</h1>

                <p>
                    Review all submitted scores and remove records
                    created during testing.
                </p>
            </div>

            <div class="admin-header-stat">
                <span>Total scores</span>
                <strong><?= count($scores) ?></strong>
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

        <section class="admin-card">

            <div class="admin-card-header">
                <div>
                    <h2>Score Records</h2>

                    <p>
                        Deleting a score is permanent and cannot be
                        reversed.
                    </p>
                </div>
            </div>

            <?php if ($scores === []): ?>

                <div class="admin-empty-state">
                    <i
                        class="bi bi-clipboard-data"
                        aria-hidden="true"
                    ></i>

                    <h3>No scores found</h3>

                    <p>
                        Submitted scores will appear here.
                    </p>
                </div>

            <?php else: ?>

                <div class="admin-table-wrapper">
                    <table class="admin-table">
                        <thead>
                        <tr>
                            <?php foreach ($columnNames as $columnName): ?>
                                <th scope="col">
                                    <?= escape(
                                        ucwords(
                                            str_replace(
                                                '_',
                                                ' ',
                                                $columnName
                                            )
                                        )
                                    ) ?>
                                </th>
                            <?php endforeach; ?>

                            <th scope="col">Action</th>
                        </tr>
                        </thead>

                        <tbody>
                        <?php foreach ($scores as $score): ?>
                            <tr>
                                <?php foreach ($columnNames as $columnName): ?>
                                    <td>
                                        <?php
                                        $value =
                                            $score[$columnName] ?? null;
                                        ?>

                                        <?php if ($value === null): ?>
                                            <span class="admin-muted">
                                                —
                                            </span>
                                        <?php else: ?>
                                            <?= escape($value) ?>
                                        <?php endif; ?>
                                    </td>
                                <?php endforeach; ?>

                                <td>
                                    <form
                                        method="post"
                                        action="scores.php"
                                        class="admin-inline-form"
                                        onsubmit="return confirmScoreDeletion();"
                                    >
                                        <input
                                            type="hidden"
                                            name="csrf_token"
                                            value="<?= escape(
                                                $_SESSION['csrf_token']
                                            ) ?>"
                                        >

                                        <input
                                            type="hidden"
                                            name="score_id"
                                            value="<?= (int) $score['id'] ?>"
                                        >

                                        <button
                                            type="submit"
                                            class="admin-button admin-button-danger admin-button-small"
                                            aria-label="Delete score <?= (int) $score['id'] ?>"
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

    </main>

    </div>

</div>

<script>
function confirmScoreDeletion() {
    return window.confirm(
        'Delete this score permanently? ' +
        'Any associated score-item records will also be removed.'
    );
}
</script>

</body>
</html>