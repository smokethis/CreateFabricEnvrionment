# CreateFabricEnvironment

## Description

Creates a series of workspaces based on input, which are in turn added to a pipeline for deployment automation.

## Prerequisites

- The name of a security group to assign workspace and pipeline rights to.
- An app registration with the following API permissions:
  - Power BI Service
    - Capacity.ReadWrite.All
    - Workspace.ReadWrite.All
    - Pipeline.ReadWrite.All
    - Tenant.ReadWrite.All
  - Microsoft Graph
    - Group.Read.All

> Tenant.ReadWrite.All is only required to use one specific function which is not called under normal operations; `updatePipelineUserAsAdmin`.

Two environment variables are required to execute the code:
|--|--|
| Variable | Description |
| TENANT_ID | Tenant ID of the app registration |
| CLIENT_ID | Client ID of the app registration |

## Limitations

- Currently does not support assigning workspaces to capacities; Fabric Trial capacities can not be automated.
> Code is commented out and should in theory work, but I cannot test it.

- Only sets user rights to the Admin role for both workspaces and pipelines.
