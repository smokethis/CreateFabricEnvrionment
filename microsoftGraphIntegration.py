from msal import PublicClientApplication
import requests

def getToken():

    tenant_id = 'a6fe9bd1-f34a-415d-b3ac-30d7e3811510'
    client_id = 'bdc7fe30-d51b-460d-96ae-6f3807d60c6e'
    scopes = ['https://graph.microsoft.com/Group.Read.All']
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
        print(result.get("correlation_id"))

def getGroup(groupName):
    
    graphToken = getToken()
    #Use Microsoft Graph to get a group oid from a name
    response = requests.get(f'https://graph.microsoft.com/v1.0/groups?$filter=displayName eq \'{groupName}\'', headers = {'Authorization': 'Bearer ' + graphToken})
    if response.status_code != 200:
        error = response.content.decode()
        raise Exception('Error getting group: ' + str(response.status_code) + ' -- ' + error)
    return response