# Spark Endpoint Audit - 2026-04-26

Scope: source scan across `spark-cli`, `spark-intelligence-builder`, `spark-telegram-bot`, `domain-chip-memory`, `spark-researcher`, `spark-character`, and `spark-agent-site` for `/health`, `/config`, `/version`, bootstrap, webhook handlers, local HTTP servers, `listen()`, `createServer`, Flask/FastAPI/Express style surfaces, and installer/public bootstrap routes.

## Exposed Or Network-Relevant Surfaces

| Repo | Surface | Bind / route | Current posture | Follow-up |
| --- | --- | --- | --- | --- |
| `spark-telegram-bot` | Mission relay | `127.0.0.1:<TELEGRAM_RELAY_PORT>/health` and `/spawner-events` | Localhost only. `/spawner-events` requires `X-Spark-Telegram-Relay-Secret` when `TELEGRAM_RELAY_SECRET` is configured. Health returns runtime identity only. | Keep `/spawner-events` tied to relay secret and local bind; add chat/user correlation before exposing beyond localhost. |
| `spark-telegram-bot` | Telegram webhook mode | none in launch build | Launch mode refuses webhook configuration and uses long polling. | Keep webhook docs marked future-only until a hosted gateway exists. |
| `spark-intelligence-builder` | Discord webhook handler | `/webhooks/discord` | Route registry enforces POST-only JSON adapter webhook contract. Auth supports Discord signatures via public key or explicit legacy secret compatibility. Public errors are generic. Secrets resolve from config at request time. | Legacy secret mode should stay compatibility-only. |
| `spark-intelligence-builder` | WhatsApp webhook handler | `/webhooks/whatsapp` GET verification and POST events | Route registry separates GET provider verification from POST adapter webhook. POST uses `X-Hub-Signature-256`; verify token and app secret resolve from config at request time. | Keep tests around unresolved secret refs and invalid signatures. |
| `spark-intelligence-builder` | OAuth callback / gateway route registry | gateway route registry | Registry validates route method/auth/content-type contracts and prevents ad hoc adapter webhook shape drift. | Add audit entry whenever new gateway route classes are added. |
| `spark-agent-site` | Hosted installer | `agent.sparkswarm.ai` static installer and command metadata | Public by design. Existing installer integrity checks compare hosted script hashes with committed manifest. | Rerun `spark verify --installers --hosted-installers` after site deploys. |
| `spark-cli` | Hosted installer verifier | outbound fetch to `agent.sparkswarm.ai` | Verification only; no local listener. | Covered by installer tests. |

## No Active Listener Found In Scan

- `domain-chip-memory`: no service listener detected in source scan; hits are docs/tests/examples and provider env use.
- `spark-researcher`: no service listener detected in source scan; hits are docs/chip bootstrap helpers.
- `spark-character`: no service listener detected in source scan; hits are prompt/eval text and provider configuration.

## Per-Request Secret Resolution Notes

- Builder webhook handlers call `ConfigManager.read_env_map()` inside auth validation, so rotated Discord/WhatsApp webhook secrets are picked up per request.
- `spark-cli` resolves keychain-backed secrets when generating module envs or launching processes. Already-running child processes still need restart after secret rotation.
- `domain-chip-memory` and `spark-character` provider objects read env at construction/call boundaries rather than exposing network listeners. No stale long-lived server cache was found in this pass.

## Tests To Keep Close To These Surfaces

- `spark-telegram-bot`: `tests/launchMode.test.ts`, `tests/healthPolling.test.ts`, `tests/spawner.test.ts`.
- `spark-intelligence-builder`: `tests/test_gateway_routes.py`, `tests/test_gateway_discord_webhook.py`, `tests/test_gateway_whatsapp_webhook.py`, `tests/test_researcher_bridge_security.py`.
- `spark-cli`: `tests/test_cli.py` installer integrity, provenance report, and generated env write-boundary tests.

## Next Endpoint Hardening

1. Add chat/user correlation on the Telegram relay event path before any non-local deployment.
2. Keep all new adapter webhooks behind the route registry and require method, auth mode, and content type in tests.
3. Add a repo-level endpoint audit CI check once the public surface stabilizes.
