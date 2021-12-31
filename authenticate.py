#!/usr/bin/env python
import requests
import string
import random
import hashlib
import json
import urllib


identity="bradleycrush@gmail.com"
credential=""

letters = string.ascii_lowercase
code_verifier = ( ''.join(random.choice(letters) for i in range(86)) )
code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).hexdigest()

#print(code_verifier)
#print(code_challenge)

client_id = "ownerapi"
code_challenge_method = "S256"
redirect_uri="https://auth.tesla.com/void/callback"
response_type="code"
scope="openid email offline_access"
state="12345"
login_hint="bradleycrush@gmail.com"
query={'client_id' : 'ownerapi', 'code_challenge' : code_challenge, 'code_challenge_method' : 'S256', 'redirect_uri' : 'https://auth.tesla.com/void/callback', 'response_type' : 'code', 'scope' : 'openid email offline_access', 'state' : '1234', 'login_hint' : 'bradleycrush@gmail.com'}
response = requests.get("https://auth.tesla.com/oauth2/v3/authorize", params=query)

if response.status_code != 200:
  print('failed to communiate with api')
  exit(0)

start_index = response.text.index('<input type=\"hidden\" name=\"_csrf\" value=\"');
end_index = response.text.index('\" />', start_index)
start_index = start_index + 41
csrf = response.text[start_index:end_index]

start_index = response.text.index('<input type=\"hidden\" name=\"_phase\" value=\"');
end_index = response.text.index('\" />', start_index)
start_index = start_index + 42
phase = response.text[start_index:end_index]

start_index = response.text.index('<input type=\"hidden\" name=\"cancel\" value=\"');
end_index = response.text.index('\" />', start_index)
start_index = start_index + 42
cancel = response.text[start_index:end_index]

start_index = response.text.index('<input type=\"hidden\" name=\"transaction_id\" value=\"');
end_index = response.text.index('\" />', start_index)
start_index = start_index + 50
transaction_id = response.text[start_index:end_index]

cookie = response.headers["set-cookie"]

data={'_csrf': f"{csrf}", '_phase': f"{phase}", 'cancel':f"{cancel}", 'transaction_id':f"{transaction_id}", 'identity':f"{identity}", 'credential':f"{credential}" }
print(data)
encoded=urllib.parse.urlencode(data, doseq=True)
print(encoded)
#data='_csrf='+ csrf+'&_phase=' + phase + '&cancel='+cancel+'&transaction_id='+transaction_id+'&identity='+identity+'&credential='+credential
query={'client_id' : 'ownerapi', 'code_challenge' : code_challenge, 'code_challenge_method' : 'S256', 'redirect_uri' : 'https://auth.tesla.com/void/callback', 'response_type' : 'code', 'scope' : 'openid email offline_access', 'state' : '1234'}
headers={'Content-Type': 'application/x-www-form-urlencoded', 'Cookie':cookie}
response =requests.post("https://auth.tesla.com/oauth2/v3/authorize", params=query, data=encoded, headers=headers)

if response.status_code == 200:
  print('success')
  print(response.text)
else:
  print('failed to communiate with api')
  print(response)
  exit(0)
