# Changelog

All notable changes to the MultiFlexi MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- OAuth2 authentication support
- Connection pooling for better performance
- Metrics and monitoring endpoints
- Custom CA certificate support
- Multiple backend support with load balancing
- Improved error messages and retry logic

## [0.1.0] - 2026-02-01

### Added
- Initial release of MultiFlexi MCP Server
- Basic MCP server implementation with stdio transport
- MultiFlexi API client integration using `multiflexi-client` package
- Comprehensive tool set for MultiFlexi operations:
  - `get_app` - Get application by ID
  - `get_job` - Get job by ID
  - `create_job` - Create new jobs
  - `get_job_status` - Check job execution status
  - `get_company` - Get company information
  - `get_user` - Get user details
  - `get_runtemplate` - Get run template by ID
  - `update_runtemplate` - Update run templates
  - `request_data_export` - GDPR data export requests
  - `get_export_status` - Check export status
- Resource endpoints for listing:
  - `multiflexi://apps` - List all applications
  - `multiflexi://jobs` - List all jobs
  - `multiflexi://companies` - List all companies
  - `multiflexi://users` - List all users
  - `multiflexi://runtemplates` - List all run templates
- Environment-based configuration system
- Basic HTTP authentication support
- Comprehensive error handling with detailed error responses
- SSL verification support with configurable options
- Request timeout and retry configuration
- Debug logging capabilities
- Modular architecture with separate config, client, and server modules
- Full test suite with pytest
- Comprehensive documentation including:
  - API usage examples
  - Configuration examples for different environments
  - Docker and Kubernetes deployment examples
  - Security best practices
- Development tools configuration:
  - Black code formatting
  - isort import sorting
  - mypy type checking
  - ruff linting
  - pytest testing framework

### Technical Details
- Python 3.9+ support
- Built on Model Context Protocol (MCP) framework
- Uses `multiflexi-client` for API interactions
- Pydantic for configuration validation
- Async/await support throughout
- Proper resource management with context managers
- JSON-based communication protocol
- Structured logging with configurable levels

### Documentation
- Complete README with installation and usage instructions
- Configuration examples for various deployment scenarios
- API examples with request/response samples
- Error handling documentation
- Security considerations and best practices
- Development setup and contribution guidelines

### Testing
- Unit tests for all major components
- Configuration validation tests
- API client wrapper tests
- MCP server functionality tests
- Mock-based testing for external dependencies
- Coverage for error scenarios

### Configuration
- Environment variable based configuration
- Support for development, testing, and production environments
- Docker and Kubernetes configuration examples
- Security-focused default settings
- Flexible timeout and retry settings