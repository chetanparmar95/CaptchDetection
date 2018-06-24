import argparse
import requests
import io
import json 
from oauth2client.service_account import ServiceAccountCredentials


PROJECT_ID = 'captchadetection-8351e'
BASE_URL = 'https://firebaseremoteconfig.googleapis.com'
REMOTE_CONFIG_ENDPOINT = 'v1/projects/' + PROJECT_ID + '/remoteConfig'
REMOTE_CONFIG_URL = BASE_URL + '/' + REMOTE_CONFIG_ENDPOINT
SCOPES = ['https://www.googleapis.com/auth/firebase.remoteconfig']

# [START retrieve_access_token]
def _get_access_token():
  """Retrieve a valid access token that can be used to authorize requests.
  :return: Access token.
  """
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      'service-account.json', SCOPES)
  access_token_info = credentials.get_access_token()
  return access_token_info.access_token
# [END retrieve_access_token]

def _get():
  """Retrieve the current Firebase Remote Config template from server.
  Retrieve the current Firebase Remote Config template from server and store it
  locally.
  """
  headers = {
    'Authorization': 'Bearer ' + _get_access_token()
  }
  resp = requests.get(REMOTE_CONFIG_URL, headers=headers)

  if resp.status_code == 200:
    with io.open('config.json', 'wb') as f:
      f.write(resp.text.encode('utf-8'))

    print('Retrieved template has been written to config.json')
    print('ETag from server: {}'.format(resp.headers['ETag']))
  else:
    print('Unable to get template')
    print(resp.text)


def _publish(parameters):
  """Publish local template to Firebase server.
  Args:
    etag: ETag for safe (avoid race conditions) template updates.
        * can be used to force template replacement.
  """
  etag = 'etag-934650754557-4'
  with open('config.json', 'r', encoding='utf-8') as f:
    content = f.read()
    
  content = {"parameters": {"irctc_session": {"defaultValue": {"value": "True"}},"paytm_otp": {"defaultValue": {"value": "4578"}}}}
  content = json.dumps(content)
  headers = {
    'Authorization': 'Bearer ' + _get_access_token(),
    'Content-Type': 'application/json; UTF-8',
    'If-Match': etag
  }
  resp = requests.put(REMOTE_CONFIG_URL, data=content.encode('utf-8'), headers=headers)
  if resp.status_code == 200:
    print('Template has been published.')
    etag = resp.headers['ETag']
    print('ETag from server: {}'.format(resp.headers['ETag']))
  else:
    print('Unable to publish template.')
    print(resp.text)


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument('--action')
  parser.add_argument('--etag')
  args = parser.parse_args()

  if args.action and args.action == 'get':
    _get()
  elif args.action and args.action == 'publish' and args.etag:
    _publish(args.etag)
  else:
    print('''Invalid command. Please use one of the following commands:
python configure.py --action=get
python configure.py --action=publish --etag=<LATEST_ETAG>''')



if __name__ == '__main__':
  main()
  
  
  
  