from msal import PublicClientApplication
import requests
import json
import os

def getToken():

    tenant_id = os.environ.get('TENANT_ID')
    client_id = os.environ.get('CLIENT_ID')
    scopes = ['https://analysis.windows.net/powerbi/api/Workspace.ReadWrite.All', 
            'https://analysis.windows.net/powerbi/api/Pipeline.ReadWrite.All', 
            'https://analysis.windows.net/powerbi/api/Capacity.ReadWrite.All']
    authority = 'https://login.microsoftonline.com/' + tenant_id

    # Create a preferably long-lived app instance which maintains a token cache.
    app = PublicClientApplication(
        client_id=client_id,
        authority=authority)

    result = None

    # We now check the cache to see
    # whether we already have some accounts that the end user already used to sign in before.
    accounts = app.get_accounts()
    if accounts:
        # If so, you could then somehow display these accounts and let end user choose
        print("Pick the account you want to use to proceed:")
        for a in accounts:
            print(a["username"])
        # Assuming the end user chose this one
        chosen = accounts[0]
        # Now let's try to find a token in cache for this account
        result = app.acquire_token_silent(account=chosen)

    if not result:
        # So no suitable token exists in cache. Let's get a new one from Azure AD.
        result = app.acquire_token_interactive(scopes=scopes)
        return result["access_token"]
    if "access_token" in result:
        # print(result["access_token"])  # Yay!
        return result["access_token"]
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))  # You may need this when reporting a bug   

def getRequestType(rtype):
    match rtype:
        case 'get':
            return requests.get
        case 'post':
            return requests.post
        case 'delete':
            return requests.delete
        case _:
            raise Exception('Invalid request type')

def placePowerBICall(token, rtype, endpoint, content):

    action = getRequestType(rtype)
    response = action (f'https://api.powerbi.com/v1.0/myorg/{endpoint}', headers = {'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json'}, data = content)
    return response

def createWorkspace(token, name):
    # Create a workspace
    content = json.dumps({'name': name})
    print('Creating workspace: ' + name)
    response = placePowerBICall(token, 'post', 'groups?workspaceV2=True', content)
    if response.status_code != 200:
        error = response.content.decode()
        raise Exception('Error creating workspace: ' + name + ' : ' + str(response.status_code) + ' -- ' + error)
    return response

def assignWorkspaceRights(token, id, rights):
    # Rights is a list of json objects
    for r in rights:
        content = json.dumps(r)
        response = placePowerBICall(token, 'post', f'groups/{id}/users', content)
        if response.status_code != 200:
            error = response.content.decode()
            raise Exception('Error assigning workspace permissions: ' + str(response.status_code) + ' -- ' + error)
        return response

def getCapacitiesAsAdmin(token):
    # Get capacities
    response = placePowerBICall(token, 'get', 'admin/capacities', '')
    if response.status_code != 200:
        error = response.content.decode()
        raise Exception('Error getting capacities: ' + str(response.status_code) + ' -- ' + error)
    return response

def assignWorkspaceToCapacity(token, workspaceId, capacityId):
    # Assign workspace to capacity
    content = json.dumps({'capacityId': capacityId})
    response = placePowerBICall(token, 'post', f'groups/{workspaceId}/AssignToCapacity', content)
    if response.status_code != 200:
        error = response.content.decode()
        raise Exception('Error assigning workspace to capacity: ' + str(response.status_code) + ' -- ' + error)
    return response

def createPipeline(token, name, description):
    
    # Create a pipeline
    content = json.dumps({'displayName': name, 'description': description})
    print('Creating pipeline: ' + name)
    response = placePowerBICall(token, 'post', 'pipelines', content)
    if response.status_code != 201:
        error = response.content.decode()
        raise Exception('Error creating pipeline: ' + name + ' : ' + str(response.status_code) + ' -- ' + error)
    return response

def getPipelines(token):
    # Get pipelines
    response = placePowerBICall(token, 'get', 'pipelines', '')
    if response.status_code != 200:
        error = response.content.decode()
        raise Exception('Error getting pipelines: ' + str(response.status_code) + ' -- ' + error)
    return response

def deletePipeline(token, pipelineId):
    # Delete pipeline
    response = placePowerBICall(token, 'delete', f'pipelines/{pipelineId}', '')
    if response.status_code != 200:
        error = response.content.decode()
        raise Exception('Error deleting pipeline: ' + str(response.status_code) + ' -- ' + error)
    return response

def updatePipelineUserAsAdmin(token, pipelineId, user):
    # Update pipeline user as admin
    content = json.dumps({'principalType': 'User', 'identifier': user, 'accessRight': 'Admin'})
    response = placePowerBICall(token, 'post', f'admin/pipelines/{pipelineId}/users', content)
    if response.status_code != 200:
        error = response.content.decode()
        raise Exception('Error updating pipeline user as admin: ' + str(response.status_code) + ' -- ' + error)
    return response

def assignWorkspaceToPipeline(token, workspaceId, pipelineId, stage):
    # Assign workspace to pipeline
    content = json.dumps({'workspaceId': workspaceId})
    response = placePowerBICall(token, 'post', f'pipelines/{pipelineId}/stages/{stage}/assignWorkspace', content)
    if response.status_code != 200:
        error = response.content.decode()
        raise Exception('Error assigning workspace to pipeline: ' + str(response.status_code) + ' -- ' + error)
    return response

def assignPipelineGroup(token, pipelineId, oid, accessRight):

    # Assign user to pipeline
    content = json.dumps({'identifier': oid, 'accessRight': accessRight, 'principalType': 'Group'})
    response = placePowerBICall(token, 'post', f'pipelines/{pipelineId}/users', content)
    if response.status_code != 200:
        error = response.content.decode()
        raise Exception('Error assigning user to pipeline: ' + str(response.status_code) + ' -- ' + error)
    return response