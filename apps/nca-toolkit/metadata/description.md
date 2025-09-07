# No-Code Architects Toolkit

A comprehensive AI toolkit designed for automation and workflow management. This toolkit provides a unified API for interacting with various AI services including OpenAI, Anthropic, and Google AI services.

## Features

- **Multi-Provider AI Support**: Integrate with OpenAI, Anthropic, and Google AI services
- **Workflow Automation**: Create complex automation workflows without code
- **API Gateway**: Unified REST API for all AI services
- **Extensible Architecture**: Easy to extend with new AI providers
- **Health Monitoring**: Built-in health checks and monitoring

## Configuration

The toolkit requires at least one API key to function:
- **OpenAI API Key**: Required for OpenAI services
- **Anthropic API Key**: Optional for Claude AI services  
- **Google API Key**: Optional for Google AI services

## Usage

Once deployed, the toolkit exposes REST endpoints at:
- `/v1/toolkit/test` - Health check endpoint
- `/v1/toolkit/chat` - Chat completion endpoint
- `/v1/toolkit/images` - Image generation endpoint
- Additional endpoints for various AI operations

## Default Credentials

The application runs on port 8002 by default when deployed through Runtipi.