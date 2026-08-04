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
| Require poster presentation type
|--------------------------------------------------------------------------
*/

$selectedPresentationType = (string) (
    $_SESSION['selected_presentation_type'] ?? ''
);

if ($selectedPresentationType !== 'poster') {
    $_SESSION['error'] =
        'Please select poster presentation before continuing.';

    header('Location: select_presentation_type.php');
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
| Process presenter selection
|--------------------------------------------------------------------------
*/

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $submittedPresenterId = filter_input(
        INPUT_POST,
        'presenter',
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

        header('Location: select_poster_presenter.php');
        exit;
    }

    if (
        $submittedPresenterId === false ||
        $submittedPresenterId === null ||
        $submittedPresenterId < 1
    ) {
        $_SESSION['error'] =
            'Please select a valid poster presenter.';

        header('Location: select_poster_presenter.php');
        exit;
    }

    try {
        /*
         * Confirm that the presenter exists and is a poster presenter.
         */
        $statement = $pdo->prepare(
            'SELECT
                p.id,
                p.subtheme_id,
                p.presenter_name,
                p.institution,
                p.presentation_title,
                p.presentation_type,
                s.name AS subtheme_name
             FROM presenters AS p
             LEFT JOIN subthemes AS s
                ON s.id = p.subtheme_id
             WHERE p.id = :presenter_id
               AND p.presentation_type = :presentation_type
               AND p.is_active = 1
             LIMIT 1'
        );

        $statement->execute([
            'presenter_id' => $submittedPresenterId,
            'presentation_type' => 'poster',
        ]);

        $presenter = $statement->fetch(PDO::FETCH_ASSOC);

        if ($presenter === false) {
            $_SESSION['error'] =
                'The selected poster presenter is not available.';

            header('Location: select_poster_presenter.php');
            exit;
        }

        /*
         * Store presenter details.
         *
         * The presenter sub-theme is stored internally so the existing
         * score.php validation can continue to work, although judges do
         * not select a sub-theme for poster presentations.
         */
        $_SESSION['selected_subtheme_id'] =
            (int) $presenter['subtheme_id'];

        $_SESSION['selected_subtheme_name'] =
            (string) ($presenter['subtheme_name'] ?? '');

        $_SESSION['selected_presenter_id'] =
            (int) $presenter['id'];

        $_SESSION['selected_presenter_name'] =
            (string) $presenter['presenter_name'];

        $_SESSION['selected_presenter_institution'] =
            (string) ($presenter['institution'] ?? '');

        $_SESSION['selected_presentation_title'] =
            (string) $presenter['presentation_title'];

        unset($_SESSION['error']);

        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));

        header('Location: poster_score.php');
        exit;
    } catch (PDOException $exception) {
        error_log(
            'Poster presenter selection failed: '
            . $exception->getMessage()
        );

        $_SESSION['error'] =
            'We could not process your presenter selection. Please try again.';

        header('Location: select_poster_presenter.php');
        exit;
    }
}

/*
|--------------------------------------------------------------------------
| Retrieve all active poster presenters
|--------------------------------------------------------------------------
*/

try {
    $statement = $pdo->prepare(
        'SELECT
            p.id,
            p.subtheme_id,
            p.presenter_name,
            p.institution,
            p.presentation_title,
            p.display_order,
            s.name AS subtheme_name
         FROM presenters AS p
         LEFT JOIN subthemes AS s
            ON s.id = p.subtheme_id
         WHERE p.presentation_type = :presentation_type
           AND p.is_active = 1
         ORDER BY
            p.presenter_name ASC,
            p.presentation_title ASC'
    );

    $statement->execute([
        'presentation_type' => 'poster',
    ]);

    $presenters = $statement->fetchAll(PDO::FETCH_ASSOC);
} catch (PDOException $exception) {
    error_log(
        'Poster presenter retrieval failed: '
        . $exception->getMessage()
    );

    $presenters = [];

    $_SESSION['error'] =
        'Poster presenters could not be loaded at this time.';
}

/*
|--------------------------------------------------------------------------
| Retrieve page values
|--------------------------------------------------------------------------
*/

$error = (string) ($_SESSION['error'] ?? '');

$selectedPresenterId = (int) (
    $_SESSION['selected_presenter_id'] ?? 0
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
        content="Select the poster presentation you want to score."
    >

    <meta
        name="theme-color"
        content="#06124F"
    >

    <title>
        Select Poster Presenter | Best Practices Forum Score Card
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

        $backLink = 'select_presentation_type.php';

        include __DIR__ . '/includes/app_header.php';

        ?>

        <div class="bpf-content bpf-presenter-content">

            <div class="bpf-page-header">

                <div>

                    <p class="bpf-step-label">
                        Step 3 of 3
                    </p>

                </div>

                <?php if ($presenters !== []): ?>

                    <div class="bpf-page-search">

                        <label
                            for="bpf-presenter-search-input"
                            class="visually-hidden"
                        >
                            Search poster presenters
                        </label>

                        <div class="bpf-input-group">

                            <i
                                class="bi bi-search bpf-input-icon"
                                aria-hidden="true"
                            ></i>

                            <input
                                type="search"
                                id="bpf-presenter-search-input"
                                class="form-control bpf-input"
                                placeholder="Search..."
                                autocomplete="off"
                                aria-controls="bpf-presenter-list"
                            >

                            <button
                                type="button"
                                id="bpf-presenter-search-clear"
                                class="bpf-search-clear"
                                aria-label="Clear search"
                                hidden
                            >
                                <i
                                    class="bi bi-x-lg"
                                    aria-hidden="true"
                                ></i>
                            </button>

                        </div>

                    </div>

                <?php endif; ?>

            </div>
            
                    <h1
                        id="bpf-page-title"
                        class="bpf-title"
                    >
                        Select Presenter
                    </h1>

            <p class="bpf-description">
                Search for and select the poster presentation you would
                like to score.
            </p>

            <p
                id="bpf-presenter-search-status"
                class="bpf-search-status"
                aria-live="polite"
            ></p>

            <div class="bpf-selected-subtheme">

                <i
                    class="bi bi-easel-fill"
                    aria-hidden="true"
                ></i>

                <div>

                    <span class="bpf-selected-subtheme-label">
                        Presentation type
                    </span>

                    <strong>
                        Poster Presentation
                    </strong>

                </div>

            </div>

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

            <?php if ($presenters !== []): ?>

                <form
                    action="select_poster_presenter.php"
                    method="post"
                    class="bpf-form"
                    id="bpf-presenter-form"
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

                    <fieldset class="bpf-presenter-fieldset">

                        <legend class="visually-hidden">
                            Available poster presenters
                        </legend>

                        <div
                            class="bpf-presenter-list"
                            id="bpf-presenter-list"
                        >

                            <?php foreach ($presenters as $presenter): ?>

                                <?php
                                $presenterId =
                                    (int) $presenter['id'];

                                $presenterName =
                                    (string) $presenter['presenter_name'];

                                $institution = trim(
                                    (string) (
                                        $presenter['institution'] ?? ''
                                    )
                                );

                                $presentationTitle =
                                    (string) $presenter['presentation_title'];

                                $subthemeName = trim(
                                    (string) (
                                        $presenter['subtheme_name'] ?? ''
                                    )
                                );

                                $isChecked =
                                    $selectedPresenterId === $presenterId;

                                $searchableContent = strtolower(
                                    $presenterName
                                    . ' '
                                    . $institution
                                    . ' '
                                    . $presentationTitle
                                    . ' '
                                    . $subthemeName
                                );
                                ?>

                                <label
                                    class="bpf-presenter-option"
                                    data-presenter-search="<?= htmlspecialchars(
                                        $searchableContent,
                                        ENT_QUOTES,
                                        'UTF-8'
                                    ) ?>"
                                >

                                    <input
                                        type="radio"
                                        name="presenter"
                                        value="<?= $presenterId ?>"
                                        class="bpf-presenter-input"
                                        <?= $isChecked ? 'checked' : '' ?>
                                        required
                                    >

                                    <span class="bpf-presenter-card">

                                        <span class="bpf-presenter-avatar">

                                            <i
                                                class="bi bi-person-fill"
                                                aria-hidden="true"
                                            ></i>

                                        </span>

                                        <span class="bpf-presenter-details">

                                            <strong class="bpf-presenter-name">
                                                <?= htmlspecialchars(
                                                    $presenterName,
                                                    ENT_QUOTES,
                                                    'UTF-8'
                                                ) ?>
                                            </strong>

                                            <?php if ($institution !== ''): ?>

                                                <span class="bpf-presenter-institution">
                                                    <?= htmlspecialchars(
                                                        $institution,
                                                        ENT_QUOTES,
                                                        'UTF-8'
                                                    ) ?>
                                                </span>

                                            <?php endif; ?>

                                            <span class="bpf-presentation-title">
                                                <?= htmlspecialchars(
                                                    $presentationTitle,
                                                    ENT_QUOTES,
                                                    'UTF-8'
                                                ) ?>
                                            </span>

                                        </span>

                                        <span
                                            class="bpf-presenter-check"
                                            aria-hidden="true"
                                        >
                                            <i class="bi bi-check-circle-fill"></i>
                                        </span>

                                    </span>

                                </label>

                            <?php endforeach; ?>

                        </div>

                        <div
                            id="bpf-presenter-search-empty"
                            class="alert alert-warning bpf-alert"
                            role="status"
                            hidden
                        >
                            No poster presenters match your search.
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
                            Poster presentations use poster-specific
                            scoring criteria.
                        </span>

                    </div>

                    <button
                        type="submit"
                        class="btn bpf-btn bpf-btn-primary"
                    >

                        Start Scoring

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
                    No active poster presenters are currently available.
                </div>

                <a
                    href="select_presentation_type.php"
                    class="btn bpf-btn bpf-btn-primary"
                >
                    Select Another Presentation Type
                </a>

            <?php endif; ?>

        </div>

    </section>

</main>

<script src="assets/js/bootstrap.bundle.min.js"></script>
<script src="assets/js/app.js"></script>

<?php if ($presenters !== []): ?>

<script>
    const presenterSearchInput = document.getElementById(
        'bpf-presenter-search-input'
    );

    const presenterSearchClear = document.getElementById(
        'bpf-presenter-search-clear'
    );

    const presenterOptions = Array.from(
        document.querySelectorAll('.bpf-presenter-option')
    );

    const presenterSearchStatus = document.getElementById(
        'bpf-presenter-search-status'
    );

    const presenterSearchEmpty = document.getElementById(
        'bpf-presenter-search-empty'
    );

    function normaliseSearchText(value) {
        return value
            .toLowerCase()
            .trim()
            .replace(/\s+/g, ' ');
    }

    function filterPresenters() {
        const searchTerm = normaliseSearchText(
            presenterSearchInput.value
        );

        let visibleCount = 0;

        presenterOptions.forEach((option) => {
            const searchableText = normaliseSearchText(
                option.dataset.presenterSearch || ''
            );

            const isVisible =
                searchTerm === '' ||
                searchableText.includes(searchTerm);

            option.hidden = !isVisible;

            if (isVisible) {
                visibleCount++;
            }
        });

        presenterSearchClear.hidden = searchTerm === '';
        presenterSearchEmpty.hidden = visibleCount !== 0;

        if (searchTerm === '') {
            presenterSearchStatus.textContent = '';
            return;
        }

        presenterSearchStatus.textContent =
            visibleCount === 1
                ? '1 poster presenter found'
                : `${visibleCount} poster presenters found`;
    }

    presenterSearchInput.addEventListener(
        'input',
        filterPresenters
    );

    presenterSearchClear.addEventListener(
        'click',
        () => {
            presenterSearchInput.value = '';
            filterPresenters();
            presenterSearchInput.focus();
        }
    );
</script>

<?php endif; ?>

</body>

</html>