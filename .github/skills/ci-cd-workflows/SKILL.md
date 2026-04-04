---
name: ci-cd-workflows
description: Work safely with AniTrend CI/CD workflows. Use when changing tests, dependencies, Docker, or GitHub Actions in .github/workflows.
compatibility: Requires access to .github/workflows and repository root files.
---

# CI/CD Workflows for AniTrend

## When to use this skill
- You are modifying tests, dependencies, Docker, or GitHub Actions.
- You need to ensure CI expectations are met.

## CI: django-ci
- Workflow: .github/workflows/django-ci.yml
- Jobs: dependency-review, analyze (CodeQL), test (pytest + Django tests).
- Test environment:
  - Uses Poetry with python-version-file in pyproject.toml.
  - Copies .env.defaults to .env.
  - Requires tmp/ directory.
  - Uses Postgres service with default test credentials.

## CD: django-cd
- Workflow: .github/workflows/django-cd.yml
- Triggers: develop pushes, tags, or manual dispatch with tag input.
- Builds/pushes multi-arch images to ghcr.io/anitrend/anitrend with cache.
- Tag rules: manual input > tag ref > latest.

## Guidance
- If adding dependencies, check license constraints in dependency-review.
- If changing tests, keep both pytest and Django test suites green.
- If changing Dockerfile, consider buildx cache usage.
