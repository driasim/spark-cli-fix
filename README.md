# Spark CLI Spike

This repo is a local spike for the Spark installer and operator CLI.

Current scope:

- read `spark.toml` manifests from local Spark module repos
- resolve the `telegram-starter` bundle from a local registry
- install modules by registry name or local repo path
- write deduped starter config into `~/.spark/`
- write generated module env files into `~/.spark/config/modules/`
- route the Telegram bot token only to `spark-telegram-bot`
- run module healthchecks through `spark status`
- emit machine-readable diagnostics through `spark status --json` and `spark doctor --json`
- start and stop startable modules through `spark start` and `spark stop`

This is intentionally a local-first spike, not the final packaged installer.

## Commands

```bash
python -m spark_cli.cli list
python -m spark_cli.cli install spark-telegram-bot
python -m spark_cli.cli install C:/Users/USER/Desktop/spawner-ui
python -m spark_cli.cli setup telegram-starter --secret telegram.bot_token=<token> --secret telegram.admin_ids=<ids>
python -m spark_cli.cli status
python -m spark_cli.cli status --json
python -m spark_cli.cli doctor --json
python -m spark_cli.cli start
python -m spark_cli.cli stop
```

If another `spark` binary already exists on your machine, use:

```bash
spark-local status
```

## Registry

The local spike reads [registry.json](./registry.json). That file currently maps
the blessed starter-stack module names to local repo paths on this machine.

## Setup Notes

`setup telegram-starter` currently reads required secrets from module manifests.

For the current starter stack:

- `telegram.bot_token` is required
- `telegram.admin_ids` is required
- `telegram.webhook_secret` is optional

Generated module config is written to:

```text
~/.spark/config/modules/
```

The current supported ownership rule remains:

- only `spark-telegram-bot` gets the Telegram bot token
- `spark-intelligence-builder` and `spawner-ui` do not
