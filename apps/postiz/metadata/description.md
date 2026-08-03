# Postiz

Postiz is the ultimate AI-powered social media scheduling platform — an open-source alternative to Buffer, Hypefury, Twitter Hunter, and more.

## Features

- **AI-Powered Scheduling**: Perfect for cc-local, OpenClaw, and other AI agents
- **Multi-Platform Support**: Schedule posts across social media platforms
- **Audience Building**: Tools to capture leads and grow your business
- **CLI Interface**: Command-line control for automation and agent integration
- **Temporal Workflow Engine**: Robust task queuing and scheduling backbone
- **Redis Cache**: Fast data access and caching layer

## Stack

- **App**: `ghcr.io/gitroomhq/postiz-app:latest`
- **Database**: PostgreSQL 15 Alpine
- **Cache**: Redis 7 Alpine
- **Workflow Engine**: Temporal 1.29.0
- **Ports**: Configurable (default 4007)

## Setup

1. Install via RunTipi dashboard
2. Set your JWT secret (auto-generated) and main URL
3. Access Postiz at your configured URL
4. Configure your social media accounts in the dashboard
5. Use the CLI or web interface to schedule posts

## CLI Integration

Postiz exposes a powerful CLI perfect for AI agent integration:

```bash
# Authenticate
postiz login --url http://localhost:4007 --token <YOUR_TOKEN>

# Schedule a post
postiz publish --platform twitter --content "Hello from Postiz!" --schedule 2026-08-04T10:00:00Z

# List scheduled posts
postiz list --status scheduled

# Get analytics
postiz analytics --period last_7_days
```

## Configuration

The app uses environment variables managed by RunTipi's form system:

- **JWT Secret**: Auto-generated, used for authentication tokens
- **Main URL**: Where to access Postiz (e.g., `http://localhost:4007`)

## Data Persistence

Data is persisted in Docker volumes:
- `postiz-postgres-data`: Application database
- `temporal-postgres-data`: Temporal workflow state
- `postiz-uploads`: Uploaded media files