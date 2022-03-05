import json

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import settings


def Create_Service(api_service_credentials: dict, api_service_name, api_version, scopes):
    # example api_service_credentials = settings.spreadsheet_creds

    flow = InstalledAppFlow.from_client_config(api_service_credentials, scopes)
    cred = flow.run_local_server()

    # cred = Credentials.from_authorized_user_info(info=json.loads(api_service_credentials), scopes=scopes)


    # if not cred or not cred.valid:
    #     if cred and cred.expired and cred.refresh_token:
    #         cred.refresh(Request())
    #     else:
    #         flow = InstalledAppFlow.from_client_config(cred.to_json(), scopes)
    #         cred = flow.run_local_server()

    print(cred)

    # try:
    #     service = build(api_service_name, api_version, credentials=cred)
    #     print(api_service_name, 'service created successfully')
    #     return service
    # except Exception as e:
    #     print('Unable to connect.')
    #     print(e)
    #     return None