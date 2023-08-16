# CreateFabricEnvironment

## Description

Creates a series of workspaces based on input, which are in turn added to a pipeline for deployment automation.

## Prerequisites

- The name of a security group to assign workspace and pipeline rights to.
- A user with Power Platform Admin rights or better.
- An app registration with the following API permissions:
  - Power BI Service
    - Capacity.ReadWrite.All
    - Workspace.ReadWrite.All
    - Pipeline.ReadWrite.All
    - Tenant.ReadWrite.All
  - Microsoft Graph
    - Group.Read.All
- Power BI tenant settings must allow the use of service principals to use Power BI APIs (<https://go.microsoft.com/fwlink/?linkid=2055030>)??????????

> Tenant.ReadWrite.All is only required to use one specific function which is not called under normal operations; `updatePipelineUserAsAdmin`.

No client secret is required for the app registration as the code must run under a users' delegated permissions.

Two environment variables are required to execute the code:

| Variable | Description |
| --- | --- |
| TENANT_ID | Tenant ID of the app registration |
| CLIENT_ID | Client ID of the app registration |

## Limitations

- Currently does not support assigning workspaces to capacities; Fabric trial capacities can not be automated through API calls due to a lack of support for rights assignment to a trial capacity.
> Code is commented out and should in theory work, but I cannot test it.

- Only sets user rights to the Admin role for both workspaces and pipelines.