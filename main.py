import base64
import json
import requests

# your unique identifier (provided by IAG)
CLIENT_ID = ""

# your unique secret (provided by IAG)
CLIENT_SECRET = ""

# the target API's unique identifier (provided by IAG)
TARGET_API_ID = ""

# A comma separated list of permissions required (provided by IAG)
PERMISSIONS = ""


# Connect to the EPortalAuth API endpoints to
# obtain a 1 hour timed bearer token.
def obtain_bearer_token():
    encoded = base64.b64encode(b'%s:%s' % (CLIENT_ID, CLIENT_SECRET))

    response = requests.post(
        'https://eportalauth.com/oauth2/token',
        headers={
            'Authorization': 'Basic %s' % (encoded,),
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        data={
            'grant_type': 'client_credentials',
            'scope': 'target-entity:%s:%s' % (TARGET_API_ID, PERMISSIONS)
        }
    )

    if response.status_code <= 299:
        return json.loads(response.text)["access_token"]
    raise Exception("could not obtain Bearer Token")


bearer_token = obtain_bearer_token()

requests.get(
    'https://test.com/sample/api/endpoint',
    headers={
        'Authorization': 'Bearer %s' % (bearer_token,)
    }
)

requests.post(
    'https://test.com/sample/api/endpoint',
    headers={
        'Authorization': 'Bearer %s' % (bearer_token,),
        'Content-Type': 'application/json'
    },
    json={
        'sample': 'json'
    }
)