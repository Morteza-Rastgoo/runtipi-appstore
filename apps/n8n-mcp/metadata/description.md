# n8n MCP Server

The n8n Model Context Protocol (MCP) server enables AI assistants like Claude Desktop, Claude Code, Windsurf, and Cursor to seamlessly build and execute n8n workflows through natural language conversation.

## Features

- **AI-Powered Workflow Creation**: Build complex automation workflows through simple chat
- **Real-time Execution**: Execute workflows and get immediate results
- **Comprehensive Integration**: Access all n8n nodes and functionality
- **Multi-AI Support**: Works with Claude Desktop, Claude Code, Windsurf, Cursor
- **Secure API**: Token-based authentication with your n8n instance

## Prerequisites

- Running n8n instance (accessible via URL)
- n8n API token (generated in n8n Settings > API)

## Configuration

1. **n8n API Base URL**: Your n8n instance URL (e.g., https://n8n.khosousi.com)
2. **n8n API Token**: Authentication token from your n8n settings
3. **Server Port**: Port for the MCP server (default: 8216)

## Usage with AI Tools

After installation, configure your AI tools to connect to this MCP server:

### Claude Desktop Configuration
Add to your Claude Desktop configuration:
```json
{
  "mcpServers": {
    "n8n": {
      "command": "npx",
      "args": ["-y", "@n8n-mcp/server"],
      "env": {
        "N8N_BASE_URL": "https://n8n-mcp.your-domain.com",
        "N8N_API_TOKEN": "your-token"
      }
    }
  }
}
```

### Example Workflows

- "Create a workflow to sync Notion to Google Sheets"
- "Build an automation to process incoming webhooks"
- "Set up monitoring workflows for system health"

## Security

- API tokens are securely stored
- All communications use HTTPS when properly configured
- No direct database access required

For more information, visit: https://www.n8n-mcp.com/
