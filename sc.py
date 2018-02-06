from sgqlc.endpoint.http import HTTPEndpoint
import json

url = 'https://oauth.authing.cn/graphql'
# headers = {'Authorization': 'bearer TOKEN'}
headers = {}

query = '''
    query getOAuthList($clientId: String!) {
        ReadOauthList(clientId: $clientId) {
            _id
            name
            image
            description
            enabled
            client
            user
            oAuthUrl
        }
    }
'''
variables = {'clientId': '59f86b4832eb28071bdd9214'}

endpoint = HTTPEndpoint(url, headers)
data = endpoint(query, variables)

print(json.dumps(data))