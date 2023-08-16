import powerBiApiIntegration as pbi

def main():

    # Get access token
    token = pbi.getToken()

    # Create a workspace
    workspaceId = pbi.createWorkspace(token, 'test').json()['id']
    print(workspaceId)

    # Assign rights to workspace
    rights = [{'groupUserAccessRight': 'Admin', 'emailAddress': 'fabrictester@rapidgrill.co.uk'}]
    pbi.assignWorkspaceRights(token, workspaceId, rights)

    # Create a pipeline
    pipelineId = pbi.createPipeline(token, 'testPipeline', 'This is a test pipeline').json()['id']

    # Assign user to pipeline
    pbi.assignPipelineUser(token, pipelineId, 'fabrictester@rapidgrill.co.uk', 'Admin')

    # Assign workspace to pipeline
    pbi.assignWorkspaceToPipeline(token, workspaceId, pipelineId, 0)

main()