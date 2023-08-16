# CreateFabricEnvironment

## Description

Creates a series of workspaces based on input, which are in turn added to a pipeline for deployment automation.

## Prerequisites

Requires the presence of a security group to assign workspace and pipeline rights to.

## Limitations

- Currently does not support assigning workspaces to capacities; Fabric Trial capacities can not be automated.
> Code is commented out and should in theory work, but I cannot test it.

- Only sets user rights to the Admin role for both workspaces and pipelines.
