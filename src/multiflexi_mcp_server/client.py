"""MultiFlexi API client wrapper for MCP Server."""

import logging
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Union

import multiflexi_client
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
    
    def get_configuration(self) -> multiflexi_client.Configuration:
        """Get configured MultiFlexi API configuration."""
        configuration = multiflexi_client.Configuration(host=self.config.host)
        
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
                result = api_instance.get_apps(format_type, limit=limit)
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
                result = api_instance.get_jobs(format_type, limit=limit)
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
        """Create a new job."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.JobApi(api_client)
                job = multiflexi_client.Job(**job_data)
                result = api_instance.add_job(job)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, "create_job")
    
    def get_job_status(self, job_id: int) -> Dict[str, Any]:
        """Get job status by ID."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.JobApi(api_client)
                result = api_instance.get_jobs_status(job_id)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, f"get_job_status({job_id})")
    
    # Company methods
    def get_companies(self, format_type: str = "json", limit: Optional[int] = None) -> Dict[str, Any]:
        """Get list of companies."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.CompanyApi(api_client)
                result = api_instance.get_companies(format_type, limit=limit)
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
                result = api_instance.get_users(format_type, limit=limit)
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
                result = api_instance.get_runtemplates(format_type, limit=limit)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, "get_runtemplates")
    
    def get_runtemplate_by_id(self, template_id: int, format_type: str = "json", limit: Optional[int] = None) -> Dict[str, Any]:
        """Get run template by ID."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.RuntemplateApi(api_client)
                result = api_instance.get_runtemplate_by_id(template_id, format_type, limit=limit)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, f"get_runtemplate_by_id({template_id})")
    
    def update_runtemplate(self, template_id: int, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update run template by ID."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.RuntemplateApi(api_client)
                update_request = multiflexi_client.UpdateRunTemplateByIdRequest(**template_data)
                result = api_instance.update_runtemplate_by_id(template_id, update_request)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, f"update_runtemplate({template_id})")
    
    # GDPR methods
    def request_data_export(self, export_type: str, format_type: str = "json") -> Dict[str, Any]:
        """Request GDPR data export."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.GdprApi(api_client)
                export_request = multiflexi_client.RequestDataExportPostRequest(
                    export_type=export_type,
                    format=format_type
                )
                result = api_instance.request_data_export(export_request)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, "request_data_export")
    
    def get_export_status(self, export_id: str) -> Dict[str, Any]:
        """Get data export status."""
        try:
            with self.get_api_client() as api_client:
                api_instance = multiflexi_client.GdprApi(api_client)
                result = api_instance.get_data_export_status(export_id)
                return self.format_response(result)
        except ApiException as e:
            return self.handle_api_error(e, f"get_export_status({export_id})")