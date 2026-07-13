# MultiFlexi MCP Server

[![PyPI version](https://badge.fury.io/py/multiflexi-mcp-server.svg)](https://badge.fury.io/py/multiflexi-mcp-server)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

MCP (Model Context Protocol) Server for MultiFlexi API integration. This server provides tools and resources for interacting with MultiFlexi applications, jobs, companies, users, and run templates.

## Features

- **Applications**: List, retrieve, and manage MultiFlexi applications
- **Jobs**: Create, retrieve, and monitor job execution
- **Companies**: Manage company data and configurations
- **Users**: Access user information and profiles
- **Run Templates**: Create and update execution templates
- **GDPR Compliance**: Request and manage data exports
- **Authentication**: Support for basic authentication
- **Error Handling**: Comprehensive error handling and logging

## Installation

### Using pip

```bash
pip install multiflexi-mcp-server
```

### From source

```bash
git clone https://github.com/VitexSoftware/multiflexi-mcp-server.git
cd multiflexi-mcp-server
pip install -e .
```

## Configuration

The server can be configured using environment variables:

### Required Configuration

- `MULTIFLEXI_HOST`: MultiFlexi API host URL (default: demo server)

### Optional Configuration

- `MULTIFLEXI_USERNAME`: Username for basic authentication
- `MULTIFLEXI_PASSWORD`: Password for basic authentication
- `MULTIFLEXI_VERIFY_SSL`: Whether to verify SSL certificates (default: true)
- `MULTIFLEXI_TIMEOUT`: Request timeout in seconds (default: 30)
- `MULTIFLEXI_MAX_RETRIES`: Maximum number of retries (default: 3)
- `MULTIFLEXI_DEBUG`: Enable debug logging (default: false)

### Example Configuration

```bash
export MULTIFLEXI_HOST="https://your-multiflexi-instance.com"
export MULTIFLEXI_USERNAME="your-username"
export MULTIFLEXI_PASSWORD="your-password"
export MULTIFLEXI_VERIFY_SSL="true"
export MULTIFLEXI_DEBUG="false"
```

## Usage

### Running the Server

```bash
multiflexi-mcp-server
```

### Claude Desktop Integration

Add the following to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows):

```json
{
  "mcpServers": {
    "multiflexi": {
      "command": "multiflexi-mcp-server",
      "env": {
        "MULTIFLEXI_HOST": "https://your-multiflexi-instance.com",
        "MULTIFLEXI_USERNAME": "your-username",
        "MULTIFLEXI_PASSWORD": "your-password"
      }
    }
  }
}
```

### Using with MCP Clients

The server provides the following resources:

- `multiflexi://apps` - List of applications
- `multiflexi://jobs` - List of jobs
- `multiflexi://companies` - List of companies
- `multiflexi://users` - List of users
- `multiflexi://runtemplates` - List of run templates

### Available Tools

#### Application Management
- `get_app` - Get application by ID
- `get_apps` - List all applications (via resources)

#### Job Management
- `get_job` - Get job by ID
- `create_job` - Create a new job
- `get_job_status` - Get job execution status
- `get_jobs` - List all jobs (via resources)

#### Company Management
- `get_company` - Get company by ID
- `get_companies` - List all companies (via resources)

#### User Management
- `get_user` - Get user by ID
- `get_users` - List all users (via resources)

#### Run Template Management
- `get_runtemplate` - Get run template by ID
- `update_runtemplate` - Update run template
- `get_runtemplates` - List all templates (via resources)

#### GDPR Compliance
- `request_data_export` - Request data export
- `get_export_status` - Check export status

### Example Tool Usage

```json
{
  "tool": "get_app",
  "arguments": {
    "app_id": 123,
    "format": "json"
  }
}
```

```json
{
  "tool": "create_job",
  "arguments": {
    "app_id": 123,
    "company_id": 456,
    "job_data": {
      "name": "Data Processing Job",
      "description": "Process daily data",
      "schedule": "0 2 * * *"
    }
  }
}
```

```json
{
  "tool": "request_data_export",
  "arguments": {
    "export_type": "personal_data",
    "format": "json"
  }
}
```

## Development

### Prerequisites

- Python 3.9+
- pip
- virtualenv (recommended)

### Setup Development Environment

```bash
git clone https://github.com/VitexSoftware/multiflexi-mcp-server.git
cd multiflexi-mcp-server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Type checking
mypy src/

# Linting
ruff src/ tests/
```

## API Documentation

This server integrates with the MultiFlexi API. For detailed API documentation, refer to:
- [MultiFlexi API Documentation](https://github.com/multiflexi/multiflexi-api)
- [OpenAPI Specification](https://virtserver.swaggerhub.com/VitexSoftware/MultiFlexi/1.0.0)

## Error Handling

The server provides comprehensive error handling:

- **API Errors**: Formatted with status codes and detailed messages
- **Authentication Errors**: Clear authentication failure messages
- **Validation Errors**: Input validation with descriptive errors
- **Network Errors**: Timeout and connection error handling

All errors are returned in a consistent JSON format:

```json
{
  "error": true,
  "operation": "get_app",
  "status": 404,
  "reason": "Not Found",
  "details": {
    "message": "Application with ID 123 not found"
  }
}
```

## Security Considerations

- **Authentication**: Use environment variables for credentials
- **SSL Verification**: Enable SSL verification in production
- **Network Security**: Ensure secure network connections
- **Data Privacy**: Handle GDPR exports with appropriate security

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/VitexSoftware/multiflexi-mcp-server/issues)
- **Documentation**: [GitHub Wiki](https://github.com/VitexSoftware/multiflexi-mcp-server/wiki)
- **Email**: info@vitexsoftware.cz

## Changelog

### v0.1.0 (Initial Release)
- Basic MCP server implementation
- MultiFlexi API integration
- Application, job, company, user, and template management
- GDPR compliance features
- Comprehensive error handling
- Environment-based configuration