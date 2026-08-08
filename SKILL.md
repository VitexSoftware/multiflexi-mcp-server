---
name: multiflexi-operations
description: Operate a MultiFlexi job scheduler instance through the multiflexi-mcp-server MCP server -- diagnose failed jobs, check whether scheduled RunTemplate obligations were fulfilled on time, and request GDPR data exports. Use when a user asks about MultiFlexi job status, failures, retries, run templates, companies, credentials, or compliance exports.
---

# MultiFlexi Operations

This skill uses the tools, resources, and prompts exposed by the
`multiflexi-mcp-server` MCP server (https://github.com/VitexSoftware/multiflexi-mcp-server)
to operate a MultiFlexi instance -- the job scheduler/middleware that runs
scheduled integrations (bank statement downloads, invoice sync, and similar
recurring jobs) for a company.

## When to use this

- A job failed and the user wants to know why, and whether it's safe to retry.
- The user wants to know whether a recurring RunTemplate's scheduled windows
  (Tasks) were actually fulfilled, fulfilled late, or missed.
- The user needs a GDPR personal-data export requested and its status tracked.
- General MultiFlexi administration: applications, companies, users, run
  templates, credentials, event sources/rules.

## Diagnosing a failed job

1. Call `get_job_status` and `get_job` for the job ID to get the exit code,
   stdout/stderr, and error details.
2. Explain the failure in plain language -- distinguish an application error
   (bad input, unreachable third-party API) from an infrastructure error
   (executor down, missing credentials).
3. Recommend whether re-running via `create_job` with the same
   `runtemplate_id` is likely to succeed, or whether something needs fixing
   first (credentials, connectivity, RunTemplate config).

The `diagnose_job_failure` MCP prompt automates this workflow -- prefer
invoking it with the job's ID over doing each step manually.

## Checking Task fulfilment

MultiFlexi tracks each scheduling window as a Task with a state:
`open`, `running`, `fulfilled`, `fulfilled_late`, `failed`, or `missed`. Use
`list_tasks` (optionally filtered by `runtemplate_id` or `state`) to see the
obligation history for a RunTemplate, and `get_task` for one Task's full job
attempt history. Call out `fulfilled_late` and `missed` Tasks specifically --
those are the windows where the obligation wasn't met on time.

The `task_fulfillment_report` MCP prompt automates a summary of this.

## Requesting a GDPR export

Call `request_data_export` (with an `export_type`, default `personal_data`),
then poll `get_export_status` until it completes. Summarize the result as a
compliance record: what was exported, when it was requested and completed,
and where it can be retrieved.

The `gdpr_export_checklist` MCP prompt automates this workflow.

## Everything else

Applications, companies, users, run templates, credentials, credential types,
topics, event sources, and event rules are all available as MCP tools and
resources -- see the server's README for the full list. Read before writing:
prefer the `list_*`/`get_*` tools to inspect current state before calling a
`set_*`/`update_*`/`create_*` tool.
