<?php
declare(strict_types=1);

session_start();

define('APP_ROOT', dirname(__DIR__));

require_once APP_ROOT . '/includes/database.php';

/*
|--------------------------------------------------------------------------
| Admin access protection
|--------------------------------------------------------------------------
|
| This assumes the admin login process will set:
|
| $_SESSION['admin_authenticated'] = true;
|
| Temporarily comment out this block while testing if the admin login has
| not yet been implemented.
|
*/

if (($_SESSION['admin_authenticated'] ?? false) !== true) {
    header('Location: login.php');
    exit;
}

/*
|--------------------------------------------------------------------------
| Ranking query
|--------------------------------------------------------------------------
|
| A presenter's final score is the average of all scores submitted by
| different judges for that presenter.
|
| COUNT(DISTINCT judge_id) protects the displayed judge count against
| accidental duplicate records.
|
*/

$sql = '
    SELECT
        p.id AS presenter_id,
        p.presenter_name,
        p.institution,
        p.presentation_title,
        LOWER(p.presentation_type) AS presentation_type,
        ROUND(AVG(s.overall_score), 2) AS average_score,
        COUNT(DISTINCT s.judge_id) AS judge_count,
        MIN(s.overall_score) AS lowest_score,
        MAX(s.overall_score) AS highest_score
    FROM scores AS s
    INNER JOIN presenters AS p
        ON p.id = s.presenter_id
    WHERE s.overall_score IS NOT NULL
      AND LOWER(p.presentation_type) IN ("oral", "poster")
    GROUP BY
        p.id,
        p.presenter_name,
        p.institution,
        p.presentation_title,
        LOWER(p.presentation_type)
    ORDER BY
        presentation_type ASC,
        average_score DESC,
        p.presenter_name ASC
';

$statement = $pdo->query($sql);

$results = $statement->fetchAll(PDO::FETCH_ASSOC);

/*
|--------------------------------------------------------------------------
| Separate oral and poster rankings
|--------------------------------------------------------------------------
*/

$oralRankings = [];
$posterRankings = [];

foreach ($results as $result) {
    $presentationType = strtolower(
        trim((string) $result['presentation_type'])
    );

    if ($presentationType === 'oral') {
        $oralRankings[] = $result;
    }

    if ($presentationType === 'poster') {
        $posterRankings[] = $result;
    }
}

/*
|--------------------------------------------------------------------------
| Add competition ranking
|--------------------------------------------------------------------------
|
| Example:
|
| 1st: 92.00
| 1st: 92.00
| 3rd: 89.00
|
| Presenters with equal averages receive the same rank.
|
*/

function addCompetitionRanks(array $rankings): array
{
    $rankedResults = [];

    $previousScore = null;
    $currentRank = 0;

    foreach ($rankings as $index => $ranking) {
        $score = round(
            (float) $ranking['average_score'],
            2
        );

        if ($previousScore === null || $score !== $previousScore) {
            $currentRank = $index + 1;
        }

        $ranking['rank_position'] = $currentRank;
        $rankedResults[] = $ranking;

        $previousScore = $score;
    }

    return $rankedResults;
}

$oralRankings = addCompetitionRanks($oralRankings);
$posterRankings = addCompetitionRanks($posterRankings);

/*
|--------------------------------------------------------------------------
| Get all presenters sharing first position
|--------------------------------------------------------------------------
*/

function getTopPresenters(array $rankings): array
{
    if ($rankings === []) {
        return [];
    }

    $highestScore = round(
        (float) $rankings[0]['average_score'],
        2
    );

    return array_values(
        array_filter(
            $rankings,
            static fn (array $ranking): bool =>
                round(
                    (float) $ranking['average_score'],
                    2
                ) === $highestScore
        )
    );
}

$topOralPresenters = getTopPresenters($oralRankings);
$topPosterPresenters = getTopPresenters($posterRankings);

function escape(string|null $value): string
{
    return htmlspecialchars(
        $value ?? '',
        ENT_QUOTES,
        'UTF-8'
    );
}

function formatScore(float|string $score): string
{
    return number_format(
        (float) $score,
        2
    ) . '%';
}

function rankLabel(int $rank): string
{
    return match ($rank) {
        1 => '1st',
        2 => '2nd',
        3 => '3rd',
        default => $rank . 'th',
    };
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">

    <meta
        name="viewport"
        content="width=device-width, initial-scale=1.0"
    >

    <title>Admin Dashboard | Score Card</title>

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

            <a
                href="index.php"
                class="admin-sidebar__link admin-sidebar__link--active"
                aria-current="page"
            >
                <i
                    class="bi bi-speedometer2"
                    aria-hidden="true"
                ></i>

                <span>Dashboard</span>
            </a>

           <a
    href="scores.php"
    class="admin-sidebar__link"
>
    <i
        class="bi bi-clipboard-data-fill"
        aria-hidden="true"
    ></i>

    <span>Manage scores</span>
</a>

<a
    href="judges.php"
    class="admin-sidebar__link"
>
    <i
        class="bi bi-people-fill"
        aria-hidden="true"
    ></i>

    <span>Manage judges</span>
</a>

            <a
                href="create_admin.php"
                class="admin-sidebar__link"
            >
                <i
                    class="bi bi-person-plus-fill"
                    aria-hidden="true"
                ></i>

                <span>Add administrator</span>
            </a>

            <a
                href="index.php"
                class="admin-sidebar__link"
            >
                <i
                    class="bi bi-arrow-clockwise"
                    aria-hidden="true"
                ></i>

                <span>Refresh results</span>
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
                            (string) (
                                $_SESSION['admin_name']
                                ?? 'Administrator'
                            )
                        ) ?>
                    </strong>

                    <span>
                        <?= escape(
                            (string) (
                                $_SESSION['admin_email']
                                ?? ''
                            )
                        ) ?>
                    </span>

                </div>

            </div>

            <a
                href="logout.php"
                class="admin-sidebar__logout"
            >
                <i
                    class="bi bi-box-arrow-right"
                    aria-hidden="true"
                ></i>

                <span>Log out</span>
            </a>

        </div>

    </aside>

    <div class="admin-content">

        <header class="admin-topbar">

            <div>

                <p class="admin-topbar__eyebrow">
                    Presentation results
                </p>

                <h2 class="admin-topbar__title">
                    Oral and poster rankings
                </h2>

            </div>

            <div class="admin-topbar__actions">

                <span class="admin-topbar__status">
                    <i
                        class="bi bi-circle-fill"
                        aria-hidden="true"
                    ></i>

                    Live results
                </span>

                <div class="admin-topbar__date">
                    <i
                        class="bi bi-calendar3"
                        aria-hidden="true"
                    ></i>

                    <?= escape(date('d F Y, H:i')) ?>
                </div>

            </div>

        </header>

        <main class="admin-main">

            <section class="admin-page-heading">

                <div>

                    <p class="admin-page-heading__label">
                        Final rankings
                    </p>

                    <h3 class="admin-page-heading__title">
                        Presentation leaders
                    </h3>

                    <p class="admin-page-heading__description">
                        Final scores are calculated from the average of all
                        judges who submitted a score for each presenter.
                    </p>

                </div>

            </section>

            <section class="winner-grid">

                <?php
                renderWinnerCard(
                    'Oral Presentation',
                    $topOralPresenters,
                    'bi-mic-fill',
                    'winner-card--oral'
                );

                renderWinnerCard(
                    'Poster Presentation',
                    $topPosterPresenters,
                    'bi-easel2-fill',
                    'winner-card--poster'
                );
                ?>

            </section>

            <section class="ranking-grid">

                <?php
                renderRankingTable(
                    'Oral Presentation Rankings',
                    $oralRankings,
                    'oral'
                );

                renderRankingTable(
                    'Poster Presentation Rankings',
                    $posterRankings,
                    'poster'
                );
                ?>

            </section>

        </main>

    </div>

</div>

</body>
</html>

<?php

/*
|--------------------------------------------------------------------------
| Winner card component
|--------------------------------------------------------------------------
*/

function renderWinnerCard(
    string $title,
    array $topPresenters,
    string $icon,
    string $modifierClass
): void {
    ?>
    <article class="winner-card <?= escape($modifierClass) ?>">

        <div class="winner-card__header">

            <div class="winner-card__icon">
                <i
                    class="bi <?= escape($icon) ?>"
                    aria-hidden="true"
                ></i>
            </div>

            <div>
                <p class="winner-card__label">
                    Current top scorer
                </p>

                <h3 class="winner-card__category">
                    <?= escape($title) ?>
                </h3>
            </div>

        </div>

        <?php if ($topPresenters === []): ?>

            <div class="winner-card__empty">

                <i
                    class="bi bi-hourglass-split"
                    aria-hidden="true"
                ></i>

                <p>No submitted scores are available yet.</p>

            </div>

        <?php else: ?>

            <?php foreach ($topPresenters as $index => $presenter): ?>

                <?php if ($index > 0): ?>
                    <div class="winner-card__tie-divider">
                        Joint winner
                    </div>
                <?php endif; ?>

                <div class="winner-card__result">

                    <div class="winner-card__presenter">

                        <div class="winner-card__position">
                            <i
                                class="bi bi-trophy-fill"
                                aria-hidden="true"
                            ></i>
                        </div>

                        <div>
                            <h4 class="winner-card__name">
                                <?= escape(
                                    (string) $presenter['presenter_name']
                                ) ?>
                            </h4>

                            <?php if (
                                trim(
                                    (string) $presenter['institution']
                                ) !== ''
                            ): ?>
                                <p class="winner-card__institution">
                                    <?= escape(
                                        (string) $presenter['institution']
                                    ) ?>
                                </p>
                            <?php endif; ?>
                        </div>

                    </div>

                    <div class="winner-card__score">
                        <?= formatScore(
                            $presenter['average_score']
                        ) ?>
                    </div>

                </div>

                <?php if (
                    trim(
                        (string) $presenter['presentation_title']
                    ) !== ''
                ): ?>
                    <p class="winner-card__presentation-title">
                        <?= escape(
                            (string) $presenter['presentation_title']
                        ) ?>
                    </p>
                <?php endif; ?>

                <div class="winner-card__meta">

                    <span>
                        <i
                            class="bi bi-people-fill"
                            aria-hidden="true"
                        ></i>

                        <?= (int) $presenter['judge_count'] ?>

                        <?= (int) $presenter['judge_count'] === 1
                            ? 'judge'
                            : 'judges' ?>
                    </span>

                    <span>
                        Score range:
                        <?= formatScore($presenter['lowest_score']) ?>
                        –
                        <?= formatScore($presenter['highest_score']) ?>
                    </span>

                </div>

            <?php endforeach; ?>

            <?php if (count($topPresenters) > 1): ?>
                <div class="winner-card__tie-notice">
                    <i
                        class="bi bi-info-circle-fill"
                        aria-hidden="true"
                    ></i>

                    <?= count($topPresenters) ?>
                    presenters currently share the highest average score.
                </div>
            <?php endif; ?>

        <?php endif; ?>

    </article>
    <?php
}

/*
|--------------------------------------------------------------------------
| Ranking table component
|--------------------------------------------------------------------------
*/

function renderRankingTable(
    string $title,
    array $rankings,
    string $type
): void {
    ?>
    <article class="ranking-card">

        <div class="ranking-card__header">

            <div>
                <p class="ranking-card__label">
                    Complete results
                </p>

                <h3 class="ranking-card__title">
                    <?= escape($title) ?>
                </h3>
            </div>

            <span class="ranking-card__count">
                <?= count($rankings) ?>

                <?= count($rankings) === 1
                    ? 'presenter'
                    : 'presenters' ?>
            </span>

        </div>

        <?php if ($rankings === []): ?>

            <div class="ranking-card__empty">

                <i
                    class="bi bi-clipboard-data"
                    aria-hidden="true"
                ></i>

                <p>
                    No <?= escape($type) ?> presentation scores have
                    been submitted.
                </p>

            </div>

        <?php else: ?>

            <div class="ranking-table-wrapper">

                <table class="ranking-table">

                    <thead>
                    <tr>
                        <th scope="col">Rank</th>
                        <th scope="col">Presenter</th>
                        <th scope="col">Title</th>
                        <th scope="col">Judges</th>
                        <th scope="col">Average</th>
                    </tr>
                    </thead>

                    <tbody>

                    <?php foreach ($rankings as $ranking): ?>

                        <?php
                        $rank = (int) $ranking['rank_position'];

                        $rankClass = match ($rank) {
                            1 => 'ranking-position--first',
                            2 => 'ranking-position--second',
                            3 => 'ranking-position--third',
                            default => '',
                        };
                        ?>

                        <tr>

                            <td>
                                <span
                                    class="ranking-position <?= escape($rankClass) ?>"
                                >
                                    <?= escape(rankLabel($rank)) ?>
                                </span>
                            </td>

                            <td>
                                <strong class="ranking-table__name">
                                    <?= escape(
                                        (string) $ranking['presenter_name']
                                    ) ?>
                                </strong>

                                <?php if (
                                    trim(
                                        (string) $ranking['institution']
                                    ) !== ''
                                ): ?>
                                    <span class="ranking-table__institution">
                                        <?= escape(
                                            (string) $ranking['institution']
                                        ) ?>
                                    </span>
                                <?php endif; ?>
                            </td>

                            <td class="ranking-table__title">
                                <?= escape(
                                    (string) $ranking['presentation_title']
                                ) ?>
                            </td>

                            <td>
                                <span class="judge-count">
                                    <i
                                        class="bi bi-person-check-fill"
                                        aria-hidden="true"
                                    ></i>

                                    <?= (int) $ranking['judge_count'] ?>
                                </span>
                            </td>

                            <td>
                                <strong class="ranking-table__score">
                                    <?= formatScore(
                                        $ranking['average_score']
                                    ) ?>
                                </strong>
                            </td>

                        </tr>

                    <?php endforeach; ?>

                    </tbody>

                </table>

            </div>

        <?php endif; ?>

    </article>
    <?php
}