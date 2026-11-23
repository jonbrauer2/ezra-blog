# Kitty Chronicles weekly publishing

The repository now uses one review-only publishing path for Kitty Chronicles Volume 2:

1. At **14:00 UTC every Sunday** (9:00 AM EST / 10:00 AM EDT), GitHub Actions selects the first unused passage from the curated ledger.
2. The OpenAI Responses API writes a story featuring Hadley, Grayson, Colton, and Tumbles.
3. A second model pass performs an editorial and Bible-summary review.
4. The Image API creates a 1536×1024 PNG in the existing Volume 2 illustration style.
5. Local checks validate the story, image, front matter, required characters, file paths, and passage uniqueness.
6. The workflow commits only to an `automation/kitty-chronicle-...` branch and opens a pull request.

The workflow never commits to `main`, never enables auto-merge, and never publishes a story by itself. GitHub Pages sees the new story only after a person reviews and merges the pull request.

## Required configuration

In **Repository settings → Secrets and variables → Actions**, add:

### Secret

- `OPENAI_API_KEY` — required for scheduled and manual live generation. Create a project API key at <https://platform.openai.com/api-keys>. The project must have billing enabled and access to both the configured text and image models.

### Optional secrets

- `OPENAI_PROJECT_ID` — limits requests to a specific OpenAI project.
- `OPENAI_ORG_ID` — selects an organization when the key can access more than one.
- `KITTY_GITHUB_TOKEN` — normally unnecessary. The built-in `GITHUB_TOKEN` is used by default. Add a fine-grained token only if repository or organization policy prevents the built-in token from pushing proposal branches or opening pull requests. Scope it only to this repository with **Contents: Read and write** and **Pull requests: Read and write**.

In **Repository settings → Actions → General → Workflow permissions**:

- choose **Read and write permissions**; and
- enable **Allow GitHub Actions to create and approve pull requests**.

The workflow also declares only `contents: write` and `pull-requests: write`. It does not request deployment, Pages, administration, or auto-merge permissions.

## Optional model variables

Repository variables can override the tested defaults:

- `KITTY_STORY_MODEL` — default `gpt-6.1-sol`
- `KITTY_IMAGE_MODEL` — default `gpt-image-2`
- `KITTY_IMAGE_QUALITY` — default `high`

Use models available to the OpenAI project. Changing model variables does not bypass any local or editorial validation.

## Manual test

Open **Actions → Propose weekly Kitty Chronicle → Run workflow**.

- Choose **dry-run** to test the complete local generator, PNG creation, ledger update, and validators without an OpenAI call and without changing the repository.
- Choose **create-pr** to run the real text and image APIs and open a review pull request.
- `passage_id` is optional. It must identify an unused candidate in `_data/kitty_chronicles_passages.json`.

The workflow refuses to spend API credits when another open `automation/kitty-chronicle-...` pull request is already waiting for review. Merge or close that proposal first.

## Review checklist

Before merging a weekly proposal:

- Read the story for biblical fidelity, age-appropriate tone, and family details.
- Inspect the illustration for character consistency and any unwanted text or artifacts.
- Confirm the pull request checks pass.
- Merge only when the story is ready for the public site.

Closing a proposal leaves its passage unused on `main`, so a future run may select it again. Merging adds the passage to the `used` ledger and makes repetition fail validation.

## Repository components

- `.github/workflows/weekly-kitty-chronicles.yml` — Sunday scheduler, manual trigger, generation, and pull-request creation.
- `.github/workflows/kitty-chronicles-ci.yml` — unit tests and repository validation for changes and proposals.
- `scripts/kitty_chronicles_generator.py` — generation, image creation, formatting, and validation.
- `_data/kitty_chronicles_passages.json` — used-passage ledger and unused candidate catalog.
- `tests/test_kitty_chronicles.py` — deterministic no-cost coverage for generation and safety checks.

The four existing Volume 2 stories are preloaded in the used ledger. The candidate catalog contains factual summaries so the writer and editorial reviewer receive a bounded source outline rather than choosing an untracked passage.
