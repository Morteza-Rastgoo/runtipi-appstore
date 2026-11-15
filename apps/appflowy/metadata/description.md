# AppFlowy

Self-hosted collaborative workspace — a Notion alternative

## Overview

AppFlowy is an open-source, self-hosted collaborative productivity workspace for notes, tasks, and databases, with AI. A self-hosted alternative to Notion and Coda. This is the full AppFlowy Cloud stack (web, API, auth, search, AI, object storage).

## Notes

- Full AppFlowy Cloud stack (11 services). The nginx entry point needs an nginx.conf that routes to appflowy_cloud/gotrue/web — supply it in the appflowy-nginx-conf volume. AI features are disabled by default (no OpenAI key).

## Links

- Source: https://github.com/AppFlowy-IO/AppFlowy-Cloud
- Website: https://appflowy.com/
