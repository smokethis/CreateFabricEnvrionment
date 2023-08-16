# CreateFabricEnvironment

## Description

Creates a series of workspaces based on input, which are in turn added to a pipeline for deployment automation.

## Prerequisites

- The name of a security group to assign workspace and pipeline rights to.
- A user with Power Platform Admin rights or better.
- An app registration with the following API permissions:
  - Power BI Service
    - Capacity.ReadWrite.All (Delegated)
    - Workspace.ReadWrite.All (Delegated)
    - Pipeline.ReadWrite.All (Delegated)
    - Tenant.ReadWrite.All (Delegated)
  - Microsoft Graph
    - Group.Read.All (Delegated)

No client secret is required for the app registration as the code must run under a users' identity and use delegated grants, application grants are only supported for Tenant.Read.All and Tenant.ReadWrite.All permissions. The user being delegated from must also have appropriate rights for the Power BI Service and Microsoft Graph.

Two environment variables are required to execute the code:

| Variable | Description |
| --- | --- |
| TENANT_ID | Tenant ID of the app registration |
| CLIENT_ID | Client ID of the app registration |

## Limitations

- Currently does not support assigning workspaces to capacities; Fabric trial capacities can not be automated through API calls due to a lack of support for rights assignment to a trial capacity.
> Code is commented out and should in theory work, but I cannot test it.

- Only supports assigning Admin rights to a single user for pipelines. This is due to the fact that pipelines only support an `Admin` role - <https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/understand-the-deployment-process#permissions>