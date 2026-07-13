# Changelog

All notable changes to the MultiFlexi MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed
- Console script entry point (`multiflexi-mcp-server`) was `async def main()`, which the
  generated script called without awaiting -- it printed an unawaited-coroutine warning
  and exited immediately without ever starting the server. `main()` is now a sync wrapper
  around `asyncio.run(run_server())`.
- `MultiFleXiClient.get_configuration()` constructed `multiflexi_client.Configuration`,
  which resolves to an unrelated domain model (app configuration record: id/app_id/name/value)
  due to a name collision in `multiflexi_client`'s top-level exports, not the API connection
  settings class. Every API call failed with a pydantic `ValidationError` as soon as
  `username`/`password` were assigned. Now imports `multiflexi_client.configuration.Configuration`
  explicitly.
- `client.py` called API methods that do not exist on `multiflexi-client` 1.1.0
  (`AppApi.get_apps`, `JobApi.get_jobs`/`add_job`/`get_jobs_status`,
  `CompanyApi.get_companies`, `UserApi.get_users`, `RuntemplateApi.get_runtemplates`/
  `get_runtemplate_by_id`/`update_runtemplate_by_id`, `GdprApi.get_data_export_status`),
  so every tool and resource crashed against the real API. Renamed to the real methods
  (`list_apps`, `listjobs`, `list_companies`, `list_users`, `list_run_templates`,
  `get_run_template_by_id`, `update_run_template_by_id`) and fixed `RequestDataExportPostRequest`
  usage.
- `get_job_status` now derives status from `Job.begin`/`end`/`exitcode` -- the real API
  has no per-job status endpoint (`DefaultApi.get_jobs_status` returns aggregate stats
  across all jobs, not one job).
- `create_job` now returns an explicit `not_supported_by_client_sdk` error instead of
  silently creating an empty job: `multiflexi-client` 1.1.0's create/update job endpoint
  (`JobApi.setjob_by_id`) has no request-body parameter, so job data could never reach
  the server.

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