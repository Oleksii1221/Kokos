# Architecture Decision Records

## ADR 001: Polling-first Telegram Runtime

Status: accepted

Kokos starts with Telegram polling instead of webhooks. Polling is simpler for
small self-hosted deployments because it does not require public HTTPS, reverse
proxy setup, or certificate management.

Webhook mode may be added later for larger deployments.

## ADR 002: Docker Compose as the Primary Deployment Unit

Status: accepted

The project ships as a Docker Compose stack with bot, PostgreSQL, and Redis.
This keeps setup repeatable on Windows and Linux servers while preserving a
clear path to more advanced infrastructure.

## ADR 003: Telegram File Cache

Status: accepted

Kokos stores Telegram `file_id` values for processed links. This improves
latency, reduces platform download pressure, and lowers server resource usage
for repeated links.

