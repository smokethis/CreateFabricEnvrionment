from msal import PublicClientApplication
import requests
import json

def getToken():

    tenant_id = 'a6fe9bd1-f34a-415d-b3ac-30d7e3811510'
    client_id = 'bdc7fe30-d51b-460d-96ae-6f3807d60c6e'
    scopes = ['https://analysis.windows.net/powerbi/api/Workspace.ReadWrite.All', 'https://analysis.windows.net/powerbi/api/Pipeline.ReadWrite.All']
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
    if "access_token" in result:
        # print(result["access_token"])  # Yay!
        pass
    else:
        print(result.get("error"))
        print(result.get("error_description"))
        print(result.get("correlation_id"))  # You may need this when reporting a bug

    return result["access_token"]

def getRequestType(rtype):
    match rtype:
        case 'get':
            return requests.get
        case 'post':
            return requests.post
        case 'put':
            return requests.put
        case 'patch':
            return requests.patch
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
    response = placePowerBICall(token, 'post', 'groups?workspaceV2=True', content)
    if response != 200:
        error = response.content.decode()
        raise Exception('Error creating workspace: ' + str(response.status_code) + ' -- ' + error)
    return response

def assignWorkspaceRights(token, id, rights):
    # Rights is a list of json objects
    for r in rights:
        content = json.dumps(r)
        print(content)
        response = placePowerBICall(token, 'post', f'groups/{id}/users', content)
        if response != 200:
            error = response.content.decode()
            raise Exception('Error assigning workspace permissions: ' + str(response.status_code) + ' -- ' + error)
        return response

def createPipeline(token, name, description):
    
    # Create a pipeline
    content = json.dumps({'name': name, 'description': description})
    response = placePowerBICall(token, 'post', 'pipelines', content)
    if response != 200:
        error = response.content.decode()
        raise Exception('Error creating pipeline: ' + str(response.status_code) + ' -- ' + error)
    return response

def assignWorkspaceToPipeline(token, workspaceId, pipelineId, stage):
    # Assign workspace to pipeline
    content = json.dumps({'workspaceId': workspaceId})
    response = placePowerBICall(token, 'put', f'pipelines/{pipelineId}/stages/{stage}/assignWorkspace', content)
    if response != 200:
        error = response.content.decode()
        raise Exception('Error assigning workspace to pipeline: ' + str(response.status_code) + ' -- ' + error)
    return response

def assignPipelineUser(token, pipelineId, upn, role):

    # Assign user to pipeline
    content = json.dumps({'identifier': upn, 'role': role, 'principalType': 'User'})
    response = placePowerBICall(token, 'post', f'pipelines/{pipelineId}/users', content)
    if response != 200:
        error = response.content.decode()
        raise Exception('Error assigning user to pipeline: ' + str(response.status_code) + ' -- ' + error)
    return response