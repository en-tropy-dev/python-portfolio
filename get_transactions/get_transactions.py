import requests
import json
import uuid
from urllib.parse import urlparse
from urllib.parse import parse_qs

# getting client id

file = open("client_id.txt", "r")
client_id = file.read()
try:
    client_id = str(client_id)
except:
    print('there is an issue with file client_id.txt')
    quit()

tpp_transaction_id = '1130098822479872' #random number
X_Sandbox_User = 'SANDBOX-INDIVIDUAL-SE-1'

def issue(status_code):
    match status_code:
        case 200:
            return
        case 400:
            print('http code 400')
            quit()
        case 401:
            print('http code 401')
            quit()
        case 404:
            print('http code 404')
            quit()


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# get token

url = 'https://sandbox.handelsbanken.com/openbanking/oauth2/token/1.0'
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'grant_type': 'client_credentials', 
    'scope': 'AIS',
    'client_id': client_id
}

response = requests.post(url, headers=headers, data=data)
issue(response.status_code)

CCG_token = response.json()['access_token']
print('CGG token received')



#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
# initiate consent

tpp_request_id = str(uuid.uuid1())
url = 'https://sandbox.handelsbanken.com/openbanking/psd2/v1/consents'

headers = {
    'X-IBM-Client-Id': client_id,
    'Authorization': 'Bearer ' + CCG_token,
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Country': 'SE',
    'TPP-Request-ID': tpp_request_id,
    'TPP-Transaction-ID': tpp_transaction_id
}

json_data = {
    'access': 'ALL_ACCOUNTS'
}

response = requests.post(url, headers=headers, json=json_data)
issue(response.status_code)

try:
    consent_id = response.json()['consentId']
    print('consent id received')
except:
    print("consent id not found")
    quit()


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#redirest request

url = 'https://sandbox.handelsbanken.com/openbanking/oauth2/authorize/1.0'
redirect_url = 'https://example.com'
state = '7293595681816576' #random number
    
headers = {
    'Accept': 'application/json',
    'X-Sandbox-User': X_Sandbox_User
}

params = {
    'response_type': 'code',
    'scope': 'AIS:' + consent_id,
    'client_id': client_id,
    'state': state,
    'redirect_uri': redirect_url
}

response = requests.get(url, params = params, headers=headers, allow_redirects=False)
issue(response.status_code)

print('redirect request sent')

h = response.headers['Location']

parsed_url = urlparse(h)
code = parse_qs(parsed_url.query)['code'][0]



#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#request authorization code grant token

url = 'https://sandbox.handelsbanken.com/openbanking/oauth2/token/1.0'
headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded'
}

data = {
    'grant_type': 'authorization_code',
    'scope': 'AIS:' + consent_id,
    'client_id': client_id,
    'code': code,
    'redirect_uri': redirect_url
}

response = requests.post(url, headers=headers, data=data)
issue(response.status_code)

access_token = response.json()['access_token']
print('CG token received')


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#get accounts

tpp_request_id = str(uuid.uuid1())
url = 'https://sandbox.handelsbanken.com/openbanking/psd2/v2/accounts'

headers = {
    'X-IBM-Client-Id': client_id,
    'Authorization': 'Bearer ' + access_token,
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'TPP-Request-ID': tpp_request_id,
    'TPP-Transaction-ID': tpp_transaction_id
}

response = requests.get(url, headers=headers)
issue(response.status_code)

account_list = response.json()['accounts']
account_IDs = []

for account in account_list:
    account_IDs.append(account['accountId'])
    
print('account id received')


#\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
#get transactions

url = 'https://sandbox.handelsbanken.com/openbanking/psd2/v2/accounts/'
tpp_request_id = str(uuid.uuid1())
transactions = {}
for account_ID in account_IDs:

    headers = {
        'X-IBM-Client-Id': client_id,
        'Authorization': 'Bearer ' + access_token,
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'TPP-Request-ID': tpp_request_id,
        'TPP-Transaction-ID': tpp_transaction_id
    }

    response = requests.get(url + account_ID + '/transactions', headers=headers)
    issue(response.status_code)
    transactions[account_ID] = response.json()
    
    
with open('transactions.json', 'w') as file:
    json.dump(transactions, file, indent = 2)
    
print('file "transactions.json" prepared')

