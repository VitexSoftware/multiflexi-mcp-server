"""MultiFlexi API client wrapper for MCP Server."""

import logging
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Union

import multiflexi_client
from multiflexi_client.configuration import Configuration as MultiFlexiApiConfiguration
from multiflexi_client.rest import ApiException

from .config import MultiFleXiConfig


logger = logging.getLogger(__name__)


class MultiFleXiClient:
    """Wrapper for MultiFlexi API client with error handling and convenience methods."""

    def __init__(self, config: MultiFleXiConfig):
        """Initialize the MultiFlexi client with configuration."""
        self.config = config
        self._setup_logging()

    def _setup_logging(self):
        """Setup logging based on configuration."""
        if self.config.debug:
            logging.getLogger("multiflexi_client").setLevel(logging.DEBUG)
            logging.getLogger("urllib3").setLevel(logging.DEBUG)

    def get_configuration(self) -> MultiFlexiApiConfiguration:
        """Get configured MultiFlexi API configuration.

        Imported explicitly from ``multiflexi_client.configuration`` because
        ``multiflexi_client.Configuration`` (top-level re-export) resolves to an
        unrelated domain model (an app "Configuration" record: id/app_id/name/value),
        not the API connection settings class. Using the top-level name here silently
        constructs the wrong object and every API call fails with a pydantic
        ValidationError as soon as ``username``/``password`` are assigned.
        """
        configuration = MultiFlexiApiConfiguration(host=self.config.host)

        # Configure authentication if credentials are provided
        if self.config.has_auth():
            configuration.username = self.config.username
            configuration.password = self.config.password

        configuration.verify_ssl = self.config.verify_ssl

        return configuration
    
    @contextmanager
    def get_api_client(self):
        """Get configured MultiFlexi API client as context manager."""
        configuration = self.get_configuration()
        with multiflexi_client.ApiClient(configuration) as api_client:
            yield api_client
    
    def format_response(self, response: Any) -> Dict[str, Any]:
        """Format API response to dictionary."""
        if hasattr(response, 'to_dict'):
            return response.to_dict()
        elif hasattr(response, '__dict__'):
            return response.__dict__
        else:
            return {"response": str(response)}
    
    def handle_api_error(self, error: ApiException, operation: str) -> Dict[str, Any]:
        """Handle API exceptions and return formatted error response."""
        logger.error(f"API error in {operation}: {error}")
        
        error_data = {
            "error": True,
            "operation": operation,
            "status": getattr(error, 'status', 'unknown'),
            "reason": getattr(error, 'reason', str(error)),
            "body": getattr(error, 'body', None),
        }
        
        # Try to parse error body if available
        if hasattr(error, 'body') and error.body:
            try:
                import json
                error_data["details"] = json.loads(error.body)
            except (json.JSONDecodeError, TypeError):
                error_data["details"] = error.body
        
        return error_data
    
    # Application methods
    def get_apps(self, format_type: str = "json", limit: Optional[int] = None) -> Dict[str, Any]:
        """Get list of applications."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.AppApi(api_client)
                result = api_instance.list_apps(format_type, limit=limit)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, "get_apps")
    
    def get_app_by_id(self, app_id: int, format_type: str = "json", limit: Optional[int] = None) -> Dict[str, Any]:
        """Get application by ID."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.AppApi(api_client)
                result = api_instance.get_app_by_id(app_id, format_type, limit=limit)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, f"get_app_by_id({app_id})")
    
    # Job methods
    def get_jobs(self, format_type: str = "json", limit: Optional[int] = None) -> Dict[str, Any]:
        """Get list of jobs."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.JobApi(api_client)
                result = api_instance.listjobs(format_type, limit=limit)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, "get_jobs")

    def get_job_by_id(self, job_id: int, format_type: str = "json", limit: Optional[int] = None) -> Dict[str, Any]:
        """Get job by ID."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.JobApi(api_client)
                result = api_instance.getjob_by_id(job_id, format_type, limit=limit)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, f"get_job_by_id({job_id})")

    def create_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new job.

        Not currently supported: multiflexi-client 1.1.0's create/update endpoint
        (``JobApi.setjob_by_id``, ``POST /job/``) only ever puts ``jobId`` and
        ``limit`` on the wire -- it has no request-body parameter at all, so
        ``job_data`` (app_id, company_id, name, schedule, ...) cannot reach the
        server. Calling it anyway would silently create a job stripped of all the
        data the caller asked for, so this fails loudly instead. Revisit once the
        multiflexi-client SDK exposes a body for this endpoint.
        """
        return {
            "error": True,
            "operation": "create_job",
            "reason": "not_supported_by_client_sdk",
            "message": (
                "multiflexi-client 1.1.0's job create/update endpoint does not "
                "accept a request body, so job_data cannot be transmitted to the "
                "server. This is an upstream SDK limitation."
            ),
        }

    def get_job_status(self, job_id: int) -> Dict[str, Any]:
        """Get job status by ID.

        multiflexi-client 1.1.0 has no per-job status endpoint -- the only
        ``*_status`` call (``DefaultApi.get_jobs_status``) returns aggregate stats
        across all jobs, not one job's state. Status for a single job is derived
        here from its ``begin``/``end``/``exitcode`` fields instead.
        """
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.JobApi(api_client)
                job = api_instance.getjob_by_id(job_id, "json")
                job_dict = self.format_response(job)
                return {
                    "job_id": job_dict.get("id", job_id),
                    "status": self._derive_job_status(job_dict),
                    "begin": job_dict.get("begin"),
                    "end": job_dict.get("end"),
                    "exitcode": job_dict.get("exitcode"),
                }
        except ApiException as e:
            return self.handle_api_error(e, f"get_job_status({job_id})")

    @staticmethod
    def _derive_job_status(job_dict: Dict[str, Any]) -> str:
        """Derive a coarse status label from a Job's begin/end/exitcode fields."""
        if not job_dict.get("begin"):
            return "scheduled"
        if not job_dict.get("end"):
            return "running"
        exitcode = job_dict.get("exitcode")
        return "success" if exitcode == 0 else "failed"
    
    # Company methods
    def get_companies(self, format_type: str = "json", limit: Optional[int] = None) -> Dict[str, Any]:
        """Get list of companies."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.CompanyApi(api_client)
                result = api_instance.list_companies(format_type, limit=limit)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, "get_companies")
    
    def get_company_by_id(self, company_id: int, format_type: str = "json", limit: Optional[int] = None) -> Dict[str, Any]:
        """Get company by ID."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.CompanyApi(api_client)
                result = api_instance.get_company_by_id(company_id, format_type, limit=limit)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, f"get_company_by_id({company_id})")
    
    # User methods
    def get_users(self, format_type: str = "json", limit: Optional[int] = None) -> Dict[str, Any]:
        """Get list of users."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.UserApi(api_client)
                result = api_instance.list_users(format_type, limit=limit)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, "get_users")
    
    def get_user_by_id(self, user_id: int, format_type: str = "json", limit: Optional[int] = None) -> Dict[str, Any]:
        """Get user by ID."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.UserApi(api_client)
                result = api_instance.get_user_by_id(user_id, format_type, limit=limit)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, f"get_user_by_id({user_id})")
    
    # Run Template methods
    def get_runtemplates(self, format_type: str = "json", limit: Optional[int] = None) -> Dict[str, Any]:
        """Get list of run templates."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.RuntemplateApi(api_client)
                result = api_instance.list_run_templates(format_type, limit=limit)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, "get_runtemplates")

    def get_runtemplate_by_id(self, template_id: int, format_type: str = "json", limit: Optional[int] = None) -> Dict[str, Any]:
        """Get run template by ID."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.RuntemplateApi(api_client)
                result = api_instance.get_run_template_by_id(template_id, format_type, limit=limit)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, f"get_runtemplate_by_id({template_id})")

    def update_runtemplate(self, template_id: int, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update run template by ID.

        Note: ``UpdateRunTemplateByIdRequest`` (multiflexi-client 1.1.0) only has
        fields ``id, active, interv, name, delay, executor, cron, note`` -- it has
        no ``description``/``command``/``environment`` fields. Any such keys passed
        in ``template_data`` are silently ignored by pydantic model construction
        (the model's default ``extra="ignore"``), not rejected.
        """
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.RuntemplateApi(api_client)
                update_request = multiflexi_client.UpdateRunTemplateByIdRequest(**template_data)
                result = api_instance.update_run_template_by_id(template_id, "json", update_request)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, f"update_runtemplate({template_id})")

    # GDPR methods
    def request_data_export(self, export_type: str, format_type: str = "json") -> Dict[str, Any]:
        """Request GDPR data export.

        Note: ``GdprApi.request_data_export`` exports all data for the
        authenticated user and has no per-category selection, so ``export_type``
        is accepted for interface compatibility but is not sent to the server.
        """
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.GdprApi(api_client)
                result = api_instance.request_data_export(action="export", format=format_type)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, "request_data_export")

    def get_export_status(self, export_id: str) -> Dict[str, Any]:
        """Get data export status.

        Note: multiflexi-client 1.1.0 has no per-ID export status lookup.
        ``GdprApi.request_data_export(action="status")`` returns the authenticated
        user's export history instead; ``export_id`` is echoed back in the result
        for the caller to match against it, but is not sent to the server.
        """
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.GdprApi(api_client)
                result = api_instance.request_data_export(action="status")
                response = self.format_response(result)
                response["requested_export_id"] = export_id
                return response
        except ApiException as e:
            return self.handle_api_error(e, f"get_export_status({export_id})")