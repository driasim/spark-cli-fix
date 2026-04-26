# Spark Security Gap Tracker - 2026-04-26

This tracker is the cross-repo source of truth for the April 26 hardening pass. Keep it updated before and after each security slice so state does not disappear across repos.

## Current Status

| Area | Status | Notes |
| --- | --- | --- |
| Rotated Telegram token history check | Verified | Custom Git history scan across `spark-cli`, `spark-intelligence-builder`, `spark-telegram-bot`, `domain-chip-memory`, `spark-researcher`, `spark-character`, and `spark-agent-site` found no rotated Telegram-token prefix hits. |
| Rotated MiniMax key history check | Verified | Same history scan found no rotated MiniMax-key prefix hits. |
| Live `.env` / temp working files | Contained locally | Current-tree scan still sees local `.env`, `.env.override`, `.env.dspy.local`, and many Builder `.tmp-*` homes, but follow-up `git ls-files` and `git check-ignore` showed those paths are ignored rather than tracked. Do not print or commit their contents. |
| History rewrite | Deferred | No `git filter-repo` rewrite is planned unless a real committed secret is found. Rewriting history and force-pushing remain destructive coordinated work requiring explicit approval. |
| Blessed module commit pins | Done | `registry.json` blessed Git modules are pinned to full commits and registry validation refuses missing pins. |
| Module provenance / attestations | Started | `spark verify --provenance` reports commit-pin, signed-commit, and attestation posture in report-only mode. Signature and attestation enforcement are intentionally not breaking installs yet. |
| Private JSON linked-path protection | Done | Spark private JSON writes refuse symlink/reparse-point paths. |
| Generated env linked-path protection | Done | Generated module env writes and cleanup now use the same linked-path guard plus write-boundary checks. |
| Endpoint audit | Started | See `docs/ENDPOINT_AUDIT_2026-04-26.md`. Builder and Telegram local relay surfaces are documented with current auth posture. |
| Per-request secret resolution | Checked | Builder Discord/WhatsApp webhook secrets resolve through `ConfigManager.read_env_map()` during request handling. CLI runtime envs resolve secrets at process launch; rotation still needs restart for long-lived child processes. |
| Approval engine | Planned only | Sensitive-action approval policy is deliberately deferred. Intended scope is high-risk operations such as deletion, force-push, history rewrite, external publish, and credential mutation. |
| Docker sandbox | Deferred optional | Docker isolation should stay optional and additive. It should not be required for normal local Spark usage. |
| T11 sustained-attack tier | Deferred | Do not focus implementation now, but keep spark-character structure compatible with adding the tier later. |

## Secret Verification Notes

Non-destructive checks run on 2026-04-26:

- `git log --all --name-only` plus `git grep`-style content checks for committed `.env` paths, Telegram token shape, rotated Telegram prefix, MiniMax key shape, rotated MiniMax prefix, `sk-` style keys, JWT shape, and sensitive env names.
- Current working-tree scan excluding `.git` and large files for `.env` paths and secret-looking content.
- `git ls-files`, `git check-ignore -v`, and `git status --ignored --short` on local env/temp paths in the repos with hits.

Result:

- History scan found only example env filenames such as `.env.example` / `.env.dspy.example`; no rotated secret prefix hits.
- Working-tree hits are local ignored files or placeholder/test strings. Treat them as private local material and keep them out of commits.
- A full gitleaks baseline would still be useful before any public security claim, but the current custom scan does not justify a history rewrite.

## Remaining Work Queue

1. Run an external secret scanner such as gitleaks or trufflehog against all Spark repos and archive the sanitized summary.
2. Decide whether to delete local ignored Builder `.tmp-*` homes after exporting anything useful. This is a local destructive cleanup and should be explicit.
3. Add real Sigstore or cosign attestation metadata to each blessed module once the report-only verifier has aged safely.
4. Turn provenance enforcement on gradually: first fail only missing commit pins, then warn on unsigned commits, then require attestations for blessed modules.
5. Add narrow endpoint regression tests whenever a new HTTP listener or public route is introduced.
6. Design the approval engine for sensitive actions before touching runtime behavior.

## Destructive Actions Requiring Fresh Confirmation

- `git filter-repo`, BFG, or any history rewrite.
- Force-push after history rewrite.
- Deleting local `.env`, `.tmp-*`, state DB, or artifact directories.
- Removing production installer/autostart entries from a live machine.
