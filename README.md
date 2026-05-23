# envyzer

Compare `.env` files across environments. Catch missing or mismatched variables before they break production.

## What it does

You have `.env`, `.env.staging`, `.env.production.example`. Are they in sync? Did someone add a variable to staging but forget to document it in the example file? envcheck compares them all and tells you exactly what's wrong.

## Quick start

```bash
pip install envyzer
envcheck check .env.example .env .env.production
```

## Example output

```
┌─────────────┬──────────┬──────────────────────────────┐
│ Key         │ Issue    │ Details                      │
├─────────────┼──────────┼──────────────────────────────┤
│ DATABASE_URL│ mismatch │ example: postgres://...,      │
│             │          │ production: mysql://...       │
│ NEW_RELIC   │ missing  │ in .env but not in .env.ex..  │
│ DEBUG       │ extra    │ in .env.example but nowhere.. │
└─────────────┴──────────┴──────────────────────────────┘
```

## Features

- **Multi-file comparison** — Compare 2+ .env files at once
- **Three issue types** — missing, extra, mismatch
- **Rich terminal output** — Color-coded tables, no squinting
- **CI-friendly** — Non-zero exit on issues, perfect for CI pipelines

## Use in CI

```yaml
# GitHub Actions
- name: Check env files are in sync
  run: envcheck check .env.example .env.staging .env.production
```

## Tech stack

Python, Typer, Rich

## More tools

- [pingbot](https://github.com/shyh26/pingbot) — dead-simple cron job monitor with Telegram alerts
- [shipnotes](https://github.com/shyh26/shipnotes) — changelog generator from git history
- [tokenalyzer](https://github.com/shyh26/tokenalyzer) — AI coding token usage & cost analyzer
