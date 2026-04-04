---
name: release-automation
description: Maintain AniTrend release automation and contribution workflows. Use when modifying release-drafter or first-interaction workflows.
compatibility: Requires access to .github/workflows and .github/release-drafter-config.yml.
---

# Release Automation for AniTrend

## When to use this skill
- You are editing release-drafter configuration or workflows.
- You are adjusting contributor greeting or auto-approve behavior.

## Release drafting
- Workflow: .github/workflows/release-drafter.yml
- Config: .github/release-drafter-config.yml
- Triggers: develop pushes and PR events (opened, reopened, synchronize).

## Contribution automation
- first-time-contribution-greeting.yaml: uses actions/first-interaction@v3.
- auto-approve.yml: auto-approves renovate[bot] PRs or manual dispatch.

## Guidance
- Keep release note labeling consistent with config.
- Ensure greeting links point to valid contribution guidelines.
- For automation changes, consider permissions and event triggers.
