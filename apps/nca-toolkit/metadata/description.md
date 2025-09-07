# No-Code Architects Toolkit

A comprehensive AI toolkit designed for automation and workflow management. This toolkit provides a unified API for interacting with various AI services and cloud storage providers.

## Features

- **Multi-Provider AI Support**: Integrate with OpenAI, Anthropic, and Google AI services
- **Cloud Storage Integration**: Support for S3-compatible storage (MinIO, AWS S3, DigitalOcean Spaces) and Google Cloud Storage
- **Media Processing**: Advanced audio/video processing, transcription, and conversion capabilities
- **Workflow Automation**: Create complex automation workflows without code
- **API Gateway**: Unified REST API for all services
- **Extensible Architecture**: Easy to extend with new providers
- **Health Monitoring**: Built-in health checks and monitoring

## Configuration

### Required Configuration
- **API Key**: Required for API authentication and security

### Optional AI Providers
- **OpenAI API Key**: For OpenAI GPT models and services
- **Anthropic API Key**: For Claude AI services  
- **Google API Key**: For Google AI services

### Storage Options (Choose One)

#### S3-Compatible Storage
- **S3 Endpoint URL**: Your S3-compatible service endpoint
- **S3 Access Key**: Access key for S3 storage
- **S3 Secret Key**: Secret key for S3 storage
- **S3 Bucket Name**: Target bucket name
- **S3 Region**: Storage region (use "None" for some providers)

#### Google Cloud Storage
- **GCP Service Account JSON**: Complete JSON service account credentials
- **GCP Bucket Name**: Target GCS bucket name

#### Local Storage
- **Local Storage Path**: Custom path for temporary file storage (defaults to /app/data)

### Performance Tuning
- **Max Queue Length**: Limit concurrent tasks (0 = unlimited)
- **Gunicorn Workers**: Number of worker processes
- **Gunicorn Timeout**: Request timeout in seconds

## Usage

Once deployed, the toolkit exposes REST endpoints at:
- `/v1/toolkit/test` - Health check endpoint
- `/v1/toolkit/authenticate` - API key validation
- `/v1/media/transcribe` - Audio/video transcription
- `/v1/media/convert` - Media format conversion
- `/v1/s3/upload` - S3 file uploads
- Additional endpoints for AI services and media processing

## Default Configuration

The application runs on port 8002 by default when deployed through Runtipi, with sensible defaults for most use cases.