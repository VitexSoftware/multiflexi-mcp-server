# API Examples

This document provides detailed examples of using the MultiFlexi MCP Server tools and resources.

## Resources

### List Applications

```json
{
  "method": "resources/read",
  "params": {
    "uri": "multiflexi://apps"
  }
}
```

**Response:**
```json
{
  "apps": [
    {
      "id": 1,
      "name": "Data Processor",
      "description": "Processes daily data files",
      "version": "1.0.0",
      "enabled": true
    },
    {
      "id": 2,
      "name": "Report Generator",
      "description": "Generates monthly reports",
      "version": "2.1.0",
      "enabled": true
    }
  ]
}
```

### List Jobs

```json
{
  "method": "resources/read",
  "params": {
    "uri": "multiflexi://jobs"
  }
}
```

**Response:**
```json
{
  "jobs": [
    {
      "id": 123,
      "app_id": 1,
      "company_id": 456,
      "name": "Daily Data Processing",
      "status": "scheduled",
      "next_run": "2026-02-02T02:00:00Z"
    }
  ]
}
```

## Tools

### Get Application Details

```json
{
  "method": "tools/call",
  "params": {
    "name": "get_app",
    "arguments": {
      "app_id": 1,
      "format": "json"
    }
  }
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Data Processor",
  "description": "Processes daily data files",
  "version": "1.0.0",
  "enabled": true,
  "configuration": {
    "input_path": "/data/input",
    "output_path": "/data/output",
    "max_memory": "2GB"
  },
  "exit_codes": [
    {"code": 0, "description": "Success"},
    {"code": 1, "description": "General error"},
    {"code": 2, "description": "Input file not found"}
  ]
}
```

### Create a Job

```json
{
  "method": "tools/call",
  "params": {
    "name": "create_job",
    "arguments": {
      "app_id": 1,
      "company_id": 456,
      "job_data": {
        "name": "Weekly Report Job",
        "description": "Generates weekly sales reports",
        "schedule": "0 9 * * 1",
        "parameters": {
          "report_type": "sales",
          "format": "pdf"
        }
      }
    }
  }
}
```

**Response:**
```json
{
  "id": 789,
  "app_id": 1,
  "company_id": 456,
  "name": "Weekly Report Job",
  "description": "Generates weekly sales reports",
  "status": "created",
  "schedule": "0 9 * * 1",
  "created_at": "2026-02-01T10:30:00Z",
  "parameters": {
    "report_type": "sales",
    "format": "pdf"
  }
}
```

### Get Job Status

```json
{
  "method": "tools/call",
  "params": {
    "name": "get_job_status",
    "arguments": {
      "job_id": 789
    }
  }
}
```

**Response:**
```json
{
  "job_id": 789,
  "status": "running",
  "started_at": "2026-02-01T09:00:00Z",
  "progress": 45,
  "estimated_completion": "2026-02-01T09:15:00Z",
  "current_step": "Processing data files",
  "logs": [
    {
      "timestamp": "2026-02-01T09:00:00Z",
      "level": "INFO",
      "message": "Job started successfully"
    },
    {
      "timestamp": "2026-02-01T09:05:00Z",
      "level": "INFO",
      "message": "Processing 1000 records"
    }
  ]
}
```

### Get Company Information

```json
{
  "method": "tools/call",
  "params": {
    "name": "get_company",
    "arguments": {
      "company_id": 456,
      "format": "json"
    }
  }
}
```

**Response:**
```json
{
  "id": 456,
  "name": "Acme Corporation",
  "industry": "Manufacturing",
  "size": "large",
  "contact": {
    "email": "admin@acme.com",
    "phone": "+1-555-0123"
  },
  "settings": {
    "timezone": "UTC",
    "currency": "USD",
    "date_format": "YYYY-MM-DD"
  },
  "created_at": "2025-01-01T00:00:00Z",
  "active": true
}
```

### Update Run Template

```json
{
  "method": "tools/call",
  "params": {
    "name": "update_runtemplate",
    "arguments": {
      "template_id": 42,
      "template_data": {
        "name": "Enhanced Data Processing Template",
        "description": "Updated template with better error handling",
        "command": "python3 /app/process_data.py --input {input_path} --output {output_path}",
        "environment": {
          "PYTHONPATH": "/app/lib",
          "LOG_LEVEL": "INFO",
          "MAX_WORKERS": "4"
        },
        "timeout": 3600,
        "retry_count": 3
      }
    }
  }
}
```

**Response:**
```json
{
  "id": 42,
  "name": "Enhanced Data Processing Template",
  "description": "Updated template with better error handling",
  "command": "python3 /app/process_data.py --input {input_path} --output {output_path}",
  "environment": {
    "PYTHONPATH": "/app/lib",
    "LOG_LEVEL": "INFO",
    "MAX_WORKERS": "4"
  },
  "timeout": 3600,
  "retry_count": 3,
  "updated_at": "2026-02-01T10:45:00Z",
  "version": 2
}
```

### Request GDPR Data Export

```json
{
  "method": "tools/call",
  "params": {
    "name": "request_data_export",
    "arguments": {
      "export_type": "personal_data",
      "format": "json"
    }
  }
}
```

**Response:**
```json
{
  "export_id": "exp_2026020112345",
  "status": "pending",
  "export_type": "personal_data",
  "format": "json",
  "requested_at": "2026-02-01T12:00:00Z",
  "estimated_completion": "2026-02-01T12:30:00Z",
  "download_url": null
}
```

### Check Export Status

```json
{
  "method": "tools/call",
  "params": {
    "name": "get_export_status",
    "arguments": {
      "export_id": "exp_2026020112345"
    }
  }
}
```

**Response:**
```json
{
  "export_id": "exp_2026020112345",
  "status": "completed",
  "export_type": "personal_data",
  "format": "json",
  "requested_at": "2026-02-01T12:00:00Z",
  "completed_at": "2026-02-01T12:25:00Z",
  "download_url": "https://secure.multiflexi.com/exports/exp_2026020112345.json",
  "expires_at": "2026-02-08T12:25:00Z",
  "file_size": 1024000
}
```

## Error Handling Examples

### API Error Response

```json
{
  "error": true,
  "operation": "get_app",
  "status": 404,
  "reason": "Not Found",
  "details": {
    "message": "Application with ID 999 not found",
    "error_code": "APP_NOT_FOUND"
  }
}
```

### Authentication Error

```json
{
  "error": true,
  "operation": "get_apps",
  "status": 401,
  "reason": "Unauthorized",
  "details": {
    "message": "Invalid credentials provided",
    "error_code": "AUTH_FAILED"
  }
}
```

### Validation Error

```json
{
  "error": true,
  "operation": "create_job",
  "status": 400,
  "reason": "Bad Request",
  "details": {
    "message": "Invalid job data",
    "error_code": "VALIDATION_ERROR",
    "validation_errors": [
      {
        "field": "app_id",
        "message": "app_id is required"
      },
      {
        "field": "schedule",
        "message": "Invalid cron expression"
      }
    ]
  }
}
```

## Batch Operations

### Processing Multiple Jobs

```python
# Example Python code using the MCP client
import json
from mcp_client import Client

async def process_multiple_jobs():
    client = Client()
    
    # Get all jobs
    jobs_resource = await client.read_resource("multiflexi://jobs")
    jobs = json.loads(jobs_resource)
    
    # Check status for each job
    for job in jobs["jobs"]:
        status = await client.call_tool("get_job_status", {
            "job_id": job["id"]
        })
        print(f"Job {job['id']}: {status['status']}")
```

### Bulk Company Updates

```python
# Example bulk operation
companies_resource = await client.read_resource("multiflexi://companies")
companies = json.loads(companies_resource)

for company in companies["companies"]:
    company_details = await client.call_tool("get_company", {
        "company_id": company["id"]
    })
    
    # Process company data
    if company_details.get("active"):
        print(f"Active company: {company_details['name']}")
```

## Integration Examples

### Webhook Handler

```python
from flask import Flask, request
import asyncio
from mcp_client import Client

app = Flask(__name__)

@app.route('/webhook/job-completed', methods=['POST'])
def job_completed_webhook():
    data = request.json
    job_id = data['job_id']
    
    # Get job details
    async def get_job_info():
        client = Client()
        return await client.call_tool("get_job", {
            "job_id": job_id,
            "format": "json"
        })
    
    job_info = asyncio.run(get_job_info())
    
    # Process completed job
    print(f"Job completed: {job_info['name']}")
    
    return {'status': 'processed'}
```

### Monitoring Dashboard Data

```python
async def get_dashboard_data():
    client = Client()
    
    # Get all resources in parallel
    apps_task = client.read_resource("multiflexi://apps")
    jobs_task = client.read_resource("multiflexi://jobs")
    companies_task = client.read_resource("multiflexi://companies")
    
    apps, jobs, companies = await asyncio.gather(
        apps_task, jobs_task, companies_task
    )
    
    return {
        "apps": json.loads(apps),
        "jobs": json.loads(jobs),
        "companies": json.loads(companies)
    }
```