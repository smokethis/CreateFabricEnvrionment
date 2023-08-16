import powerBiApiIntegration as pbi
import microsoftGraphIntegration as graph

# Get access tokens
pbiToken = pbi.getToken()

def configureWorkspace(workspaceName, groupId, role):

    # Create a workspace
    workspaceId = pbi.createWorkspace(pbiToken, workspaceName).json()['id']
    print(workspaceId)

    # Assign directory group rights to workspace
    rights = [{'groupUserAccessRight': role, 'identifier': groupId, 'principalType': 'Group'}]
    pbi.assignWorkspaceRights(pbiToken, workspaceId, rights)

    # # Assign workspace to capacity
    # ## Find the Fabric Trial capacity id
    # result = pbi.getCapacitiesAsAdmin(pbiToken)
    # capacities = result.json()['value']
    # ## Find the relevant capacity id with the sku 'FT1'
    # capacityId = None
    # for c in capacities:
    #     if c['sku'] == 'FT1':
    #         capacityId = c['id']
    #         break
    # ## Use the capacity id to assign the workspace to the capacity
    # pbi.assignWorkspaceToCapacity(pbiToken, workspaceId, capacityId)

    return workspaceId

def configurePipeline(workspaces, pipelineName, pipelineDescription, groupId, role):

    # Create a pipeline
    pipelineId = pbi.createPipeline(pbiToken, pipelineName, pipelineDescription).json()['id']

    # Assign user to pipeline
    pbi.assignPipelineGroup(pbiToken, pipelineId, groupId, role)

    # Assign workspaces to pipeline
    for workspace in workspaces:
        pbi.assignWorkspaceToPipeline(pbiToken, workspace['id'], pipelineId, workspace['stage'])

def createResources(groupName, role, dataProductName, purpose):

    # Map environments to pipeline stages
    stageMap = { # environment name: pipeline stageid
        'Dev': 0,
        'Test': 1,
        'Prod': 2
    }

    # Create a list of workspaces to create based on the data product name
    workspaces = []
    for stage in stageMap.keys():
        workspaces.append({'name': 'GRP-' + dataProductName + '-' + stage, 'stage': stageMap.get(stage)})
          
    # Fetch oid of the security group to assign to the workspaces
    result = graph.getGroup(graphToken, groupName)
    groupId = result.json()['value'][0]['id']

    # Initialise list of workspace ids
    workspaceIds = []
    # Create workspaces
    for workspace in workspaces:
        workspaceId = configureWorkspace(workspace['name'], groupId, 'Admin')
        # Append this workspace id to list of workspace ids
        workspaceIds.append(workspaceId)

    for idx, wId in enumerate(workspaceIds):
        workspaces[idx]['id'] = wId

    # Can't assign workspace to capacity without admin rights, and can't assign admin rights on a Trial capacity
    # Therefore pause for capacity assignment to be done manually
    print('Workspaces created')
    print(workspaces)
    input('Press enter when capacity assignment is done')

    configurePipeline(workspaces, 'GRP-' + purpose + dataProductName, 
                      'Pipeline for ' + dataProductName + ' ' + purpose, groupId, role)

def main():
    ### Important variables ###
    groupName = '' # Name of security group to the new workspaces
    role = '' # Role to assign to this security group on both workspaces and pipeline
    dataProductName = '' # Name of the data product to create workspaces for
    purpose = '' # Purpose of the workspaces, used in pipeline name definition
    ###########################
    
    # Ask user for variables
    groupName = input('Enter the name of the security group to assign to the workspaces: ')
    role = input('Enter the role to assign to the security group on the workspaces and pipeline: ')
    dataProductName = input('Enter the name of the data product to create workspaces for: ')
    purpose = input('Enter the purpose of the workspaces (e.g. "Engineering"): ')
    
    createResources(groupName, role, dataProductName, purpose)

main()