# SurviveChef Project Tracker

This file is a working tracker for the local repo at `cits5505/` and the GitHub remote `https://github.com/xAmyyang/cits5505.git`.

It is based on the local Git checkout, remote branch references, merged PR commits on `origin/main`, and the current source tree.

## Current Snapshot

- Active branch: `main`
- Local `main` head: `4dee0d0`
- Remote tracking branch: `origin/main`
- Latest merged PR on `main`: `#85` on `2026-05-17`
- Open GitHub PRs: none as of `2026-05-17`
- Local-only untracked file:
  - `PROJECT_TRACKER.md`

## Current App Structure

Core backend files:
- `app.py`
- `db.py`
- `schema.sql`
- `seed.sql`
- `migrate.py`
- `migrations/`

Templates:
- `templates/index.html`
- `templates/login.html`
- `templates/signup.html`
- `templates/ingredient-selection.html`
- `templates/recipe-results.html`
- `templates/recipe-detail.html`
- `templates/community.html`
- `templates/share-recipe.html`
- `templates/SavedRecipe.html`
- `templates/profile.html`
- `templates/edit_profile.html`
- `templates/navbar.html`

Frontend assets:
- `static/css/`
- `static/js/`

Tests:
- `pytest.ini`
- `tests/test_app_flows.py`
- `tests/test_routes.py`
- `tests/test_selenium.py`
- `tests/conftest.py`

## Product Scope Reached So Far

The repo history and current code show that SurviveChef now includes:

- Flask application routing
- SQLite-backed persistence
- user signup, login, logout, and session handling
- ingredient-based recipe search
- "1 ingredient away" recipe suggestions
- recipe detail pages
- saved recipes flow
- liked recipes flow
- community recipe sharing
- recipe comments on recipe detail pages
- profile and edit profile pages
- database migrations
- CSRF protection for POST forms
- unit and Selenium test setup

## Merged PR Timeline

The repo uses a branch-plus-PR workflow. The entries below are reconstructed from merge commits on `origin/main`.

### Foundation and Early UI

- `#4` `2026-03-22` `amy-homepage-1.0`
  - Purpose: initial homepage implementation
  - Files landed:
    - `index.html`
    - `survivechef-animations.css`
    - `survivechef-bootstrap-theme.css`

- `#6` `2026-03-24` `jeong-readme`
  - Purpose: initial README and project definition
  - Files landed:
    - `README.md`

- `#13` `2026-04-04` `sohaib-recipe-detail`
  - Purpose: recipe detail page UI
  - Files landed:
    - `recipe-detail.css`
    - `recipe-detail.html`

- `#14` `2026-04-05` `feature/login-page-clean`
  - Purpose: login page styling and auth page logic
  - Files landed:
    - `auth.css`
    - `auth.js`
    - `login.html`

- `#15` `2026-04-05` `feature/signup-page-clean`
  - Purpose: signup page UI
  - Files landed:
    - `signup.html`

- `#18` `2026-04-05` `feature-profile`
  - Purpose: initial profile page UI
  - Files landed:
    - `profile.css`
    - `profile.html`
    - `survivechef-bootstrap-theme.css`

- `#11` `2026-04-05` `jeong/ingredient-layout`
  - Purpose: ingredient selection layout
  - Files landed:
    - `ingredient-selection.css`
    - `ingredient-selection.html`

- `#20` `2026-04-06` `jeong/chips-ui`
  - Purpose: ingredient chips styling
  - Files landed:
    - `ingredient-selection.css`

- `#23` `2026-04-06` `feature-SavedRecipe`
  - Purpose: saved recipe page UI
  - Files landed:
    - `SavedRecipe.css`
    - `SavedRecipe.html`

- `#24` `2026-04-06` `jeong/chips-interaction`
  - Purpose: ingredient chip interaction
  - Files landed:
    - `ingredient-selection.html`
    - `ingredient-selection.js`

- `#29` `2026-04-15` `fature-savedrecipe`
  - Purpose: saved recipe page refinement
  - Files landed:
    - `SavedRecipe.html`

- `#30` `2026-04-21` `feature-homepage-afterlogin`
  - Purpose: homepage login-state updates
  - Files landed:
    - `homepage.css`
    - `homepage.js`
    - `index.html`

- `#31` `2026-04-21` `feature-profile1.0`
  - Purpose: profile behavior refinement
  - Files landed:
    - `profile.html`
    - `profile.js`

- `#34` `2026-04-21` `sohaib-community-final`
  - Purpose: initial community page UI
  - Files landed:
    - `community.css`
    - `community.html`

### Flask Conversion and Backend Start

- `#35` `2026-04-25` `backend-attempt1`
  - Purpose: move frontend into backend-friendly Flask structure
  - Files landed:
    - `app.py`
    - `templates/*` for main pages
    - `static/css/*`
    - `static/js/*`

- `#37` `2026-04-27` `docs/flask-setup`
  - Purpose: local setup documentation and dependency baseline
  - Files landed:
    - `.gitignore`
    - `README.md`
    - `requirements.txt`

- `#38` `2026-04-30` `backend/flask-routing`
  - Purpose: convert major pages to Flask template routing
  - Files landed:
    - `app.py`
    - `templates/SavedRecipe.html`
    - `templates/community.html`
    - `templates/index.html`
    - `templates/ingredient-selection.html`
    - `templates/login.html`
    - `templates/profile.html`
    - `templates/recipe-detail.html`
    - `templates/signup.html`

### Recipe Data and Auth Backend

- `#41` `2026-05-02` `feature/add-recipe-json`
  - Purpose: initial recipe JSON data
  - Files landed:
    - `data/recipe.json`

- `#42` `2026-05-02` `sohaib-add-recipes-json`
  - Purpose: expanded recipe JSON dataset
  - Files landed:
    - `data/recipes.json`

- `#45` `2026-05-05` `backend-login-signup`
  - Purpose: auth backend, sessions, DB foundation
  - Files landed:
    - `.gitignore`
    - `app.py`
    - `data/recipes.json`
    - `db.py`
    - `schema.sql`
    - `static/js/auth.js`
    - `static/js/homepage.js`
    - `static/js/profile.js`
    - `templates/community.html`
    - `templates/index.html`
    - `templates/login.html`
    - `templates/profile.html`
    - `templates/recipe-detail.html`
    - `templates/signup.html`

- `#46` `2026-05-06` `ingredient-matching`
  - Purpose: recipe result matching and ingredient-selection flow
  - Files landed:
    - `app.py`
    - `static/css/recipe-results.css`
    - `static/js/ingredient-selection.js`
    - `templates/SavedRecipe.html`
    - `templates/community.html`
    - `templates/ingredient-selection.html`
    - `templates/recipe-results.html`

- `#47` `2026-05-06` `saved-recipes-backend`
  - Purpose: save and view saved recipes from backend
  - Files landed:
    - `README.md`
    - `app.py`
    - `schema.sql`
    - `static/css/ingredient-selection.css`
    - `static/css/recipe-results.css`
    - `templates/SavedRecipe.html`
    - `templates/recipe-detail.html`
    - `templates/recipe-results.html`

### SQL Migration and Shared Components

- `#48` `2026-05-09` `BackendAttemp02-AY`
  - Purpose: move app closer to SQL-backed homepage and schema
  - Files landed:
    - `app.py`
    - `schema.sql`
    - `templates/index.html`

- `#52` `2026-05-12` `remove-recipes-json`
  - Purpose: remove old JSON recipe data path
  - Files landed:
    - `data/recipe.json`
    - `data/recipes.json`

- `#54` `2026-05-12` `feature/sql-recipe-results`
  - Purpose: SQL-backed recipe results
  - Files landed:
    - `app.py`
    - `schema.sql`
    - `seed.sql`

- `#55` `2026-05-12` `feature/shared-navbar`
  - Purpose: shared navigation component across pages
  - Files landed:
    - `templates/SavedRecipe.html`
    - `templates/community.html`
    - `templates/ingredient-selection.html`
    - `templates/navbar.html`
    - `templates/profile.html`
    - `templates/recipe-results.html`

### Profile, Community, and DB Stabilization

- `#58` `2026-05-12` `profilepageBackend-ay`
  - Purpose: edit profile page and profile/backend wiring
  - Files landed:
    - `app.py`
    - `migrations/001_initial_schema.sql`
    - `migrations/002_add_profile_fields.sql`
    - `schema.sql`
    - `static/css/editprofile.css`
    - `templates/edit_profile.html`
    - `templates/profile.html`

- `#62` `2026-05-12` `BackendAttemp03`
  - Purpose: schema and profile dynamic-data fixes plus migrations
  - Files landed:
    - `app.py`
    - `migrate.py`
    - `migrations/001_initial_schema_down.sql`
    - `migrations/001_initial_schema_up.sql`
    - `migrations/002_add_profile_fields_up.sql`
    - `migrations/003_add_recipe_columns_up.sql`
    - `schema.sql`
    - `templates/profile.html`

- `#63` `2026-05-12` `feature/community-recipe-flow-main-rebuild`
  - Purpose: community recipe sharing flow rebuilt on SQL-backed app
  - Files landed:
    - `app.py`
    - `static/css/community.css`
    - `templates/community.html`
    - `templates/index.html`
    - `templates/ingredient-selection.html`
    - `templates/share-recipe.html`

- `#64` `2026-05-13` `fix/auth-db-errors`
  - Purpose: auth and DB bug fixes
  - Files landed:
    - `app.py`
    - `templates/ingredient-selection.html`

- `#65` `2026-05-13` `data/expand-recipe-seed`
  - Purpose: improve seed data and recipe query behavior
  - Files landed:
    - `app.py`
    - `seed.sql`

- `#68` `2026-05-13` `sohaib-community-final`
  - Purpose: polish community and saved recipe save/unsave flow
  - Files landed:
    - `app.py`
    - `templates/SavedRecipe.html`
    - `templates/community.html`

- `#69` `2026-05-13` `feature/test-setup`
  - Purpose: add automated testing baseline
  - Files landed:
    - `requirements.txt`
    - `tests/conftest.py`
    - `tests/test_routes.py`
    - `tests/test_selenium.py`

### Post-Testing Expansion and Final Polish

- `#70` `2026-05-14` `feature/testing-flow-coverage`
  - Purpose: expand testing coverage and pytest setup
  - Files landed:
    - `README.md`
    - `pytest.ini`
    - `requirements.txt`
    - `tests/conftest.py`
    - `tests/test_app_flows.py`
    - `tests/test_selenium.py`

- `#72` `2026-05-14` `feature/remove-social-signin-buttons-clean`
  - Purpose: remove non-functional social sign-in buttons
  - Files landed:
    - `templates/login.html`
    - `templates/signup.html`

- `#73` `2026-05-15` `sohaib-like-button-backend`
  - Purpose: add recipe likes across community, results, detail, and profile flows
  - Files landed:
    - `app.py`
    - `migrations/004_add_recipe_likes_up.sql`
    - `templates/community.html`
    - `templates/profile.html`
    - `templates/recipe-detail.html`
    - `templates/recipe-results.html`

- `#74` `2026-05-15` `improvements-ay`
  - Purpose: homepage, navbar, recipe detail, and schema polish after team discussion
  - Files landed:
    - `app.py`
    - `schema.sql`
    - `static/css/homepage.css`
    - `static/css/ingredient-selection.css`
    - `templates/index.html`
    - `templates/navbar.html`
    - `templates/recipe-detail.html`

- `#75` `2026-05-15` `sohaib-like-button-backend`
  - Purpose: add recipe comments backend wiring
  - Files landed:
    - `app.py`
    - `migrations/005_add_recipe_comments_up.sql`
    - `templates/recipe-detail.html`

- `#76` `2026-05-15` `newtestunits-ay`
  - Purpose: adjust Selenium coverage and README
  - Files landed:
    - `README.md`
    - `tests/conftest.py`
    - `tests/test_selenium.py`

- `#77` `2026-05-15` `xAmyyang-patch-1`
  - Purpose: add `recipe_comments` to the base schema
  - Files landed:
    - `schema.sql`

- `#79` `2026-05-15`
  - Status: closed without merge
  - Purpose: an earlier attempt to add CSRF tokens to POST forms

- `#80` `2026-05-16` `securityimpl02.ay`
  - Purpose: add CSRF protection and move configuration toward safer defaults
  - Files landed:
    - `.gitignore`
    - `app.py`
    - `requirements.txt`
    - `templates/SavedRecipe.html`
    - `templates/community.html`
    - `templates/edit_profile.html`
    - `templates/ingredient-selection.html`
    - `templates/login.html`
    - `templates/recipe-detail.html`
    - `templates/recipe-results.html`
    - `templates/share-recipe.html`
    - `templates/signup.html`

- `#81` `2026-05-16`
  - Status: closed without merge
  - Purpose: an earlier dependency-fix attempt later replaced by `#82`

- `#82` `2026-05-17` `fix/requirements-dependencies`
  - Purpose: fix invalid dependency versions in `requirements.txt`
  - Files landed:
    - `requirements.txt`

- `#83` `2026-05-17` `fix/csrf-test-failures`
  - Purpose: keep tests working with CSRF enabled in the app
  - Files landed:
    - `tests/conftest.py`

- `#84` `2026-05-17` `polish/final-ui-cleanup`
  - Purpose: final UI cleanup around profile, recipe detail, navbar, and branding
  - Files landed:
    - `static/css/profile.css`
    - `static/css/recipe-detail.css`
    - `static/css/survivechef-bootstrap-theme.css`
    - `templates/index.html`
    - `templates/navbar.html`
    - `templates/profile.html`
    - `templates/recipe-detail.html`

- `#85` `2026-05-17` `polish/share-recipe-placeholders`
  - Purpose: clarify ingredient placeholder text on the share recipe page
  - Files landed:
    - `templates/share-recipe.html`

## Branch and PR Status

Current remote state:

- `origin/main` is the active shared branch
- old remote feature branches have largely been deleted after merge
- there are no open GitHub pull requests as of `2026-05-17`

Important note:
- Local branches still exist for historical work, but they should not be assumed to represent active upstream work.
- The previously active branch `feature/remove-social-signin-buttons-clean` was merged as `#72`, and its remote branch has been deleted.

## Main Ownership Areas By File Pattern

Use this section as a fast map when continuing development.

- Auth and sessions:
  - `app.py`
  - `templates/login.html`
  - `templates/signup.html`
  - `static/js/auth.js`

- Ingredient selection and recipe matching:
  - `templates/ingredient-selection.html`
  - `static/js/ingredient-selection.js`
  - `templates/recipe-results.html`
  - `static/css/recipe-results.css`
  - `app.py`

- Recipe detail and saved recipes:
  - `templates/recipe-detail.html`
  - `templates/SavedRecipe.html`
  - `app.py`
  - `schema.sql`
  - `migrations/004_add_recipe_likes_up.sql`
  - `migrations/005_add_recipe_comments_up.sql`

- Community and sharing:
  - `templates/community.html`
  - `templates/share-recipe.html`
  - `static/css/community.css`
  - `app.py`

- Profile and edit profile:
  - `templates/profile.html`
  - `templates/edit_profile.html`
  - `static/css/profile.css`
  - `static/css/editprofile.css`
  - `app.py`
  - `schema.sql`
  - `migrations/`

- Shared layout:
  - `templates/navbar.html`
  - `templates/index.html`
  - `static/css/homepage.css`
  - `static/js/homepage.js`

- Database and migration layer:
  - `db.py`
  - `schema.sql`
  - `seed.sql`
  - `migrate.py`
  - `migrations/`

- Test layer:
  - `pytest.ini`
  - `tests/test_app_flows.py`
  - `tests/conftest.py`
  - `tests/test_routes.py`
  - `tests/test_selenium.py`

## Known Repo Gaps And Cautions

- Direct GitHub review comments are not available from the local Git history.
- PR titles are visible through merge commits, but inline discussion threads are not.
- Some old merge diffs reference pre-Flask root-level file names like `index.html` or `profile.html`; those correspond to files that later moved into `templates/` and `static/`.
- The README still contains some outdated wording from earlier phases of the project and should be aligned with the current Flask + SQLite implementation.
- Migration filenames are inconsistent across history:
  - current tree uses `_up.sql` and `_down.sql`
  - earlier merged history referenced older migration names without suffix pairs
- The local virtualenv must be refreshed after pulling newer `main` because recent PRs added `Flask-WTF`, `python-dotenv`, `selenium`, and related dependencies.

## Recommended Next Working Order

1. Treat `app.py`, `schema.sql`, `seed.sql`, `templates/`, and `tests/` as the primary continuation surface.
2. Update `README.md` to match the current backend, CSRF, likes, comments, and test reality.
3. Expand tests around the community flow, save/unsave flow, like flow, comment flow, and edit-profile flow before large new feature work.
4. Review `schema.sql` and `migrations/` together to make sure fresh database setup and incremental migration paths stay aligned.
5. If new features are planned, build them on the current SQL-backed routes rather than reviving old JSON-based branches.
6. Decide whether the next phase is feature work or a stabilization pass, because the repo now has more moving parts in auth, forms, and test setup.

## What To Check Before New Work Starts

- `app.py` route coverage and route responsibilities
- `schema.sql` vs `migrations/` consistency
- `seed.sql` data completeness
- current test reliability
- how CSRF, likes, and comments affect any new forms or routes
