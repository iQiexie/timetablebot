import json
from random import randint
from typing import List, Tuple, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import settings
from refactor.base.utils import safe_get_dict
from refactor.google_api.crud import GoogleApiCRUD

drive_service_args = ('drive', 'v2', ['https://www.googleapis.com/auth/drive'])
sheets_service_args = ('sheets', 'v4', ['https://www.googleapis.com/auth/spreadsheets.readonly'])


class GoogleApiHandler:
    def __init__(self, db: GoogleApiCRUD):
        self.db = db
        self.drive_service = None
        self.sheets_service = None

    async def init_services(self):
        self.drive_service = await self.create_service(*drive_service_args)
        self.sheets_service = await self.create_service(*sheets_service_args)

    @staticmethod
    async def run_server(flow):
        return flow.run_local_server(port=randint(5, 1000))

    async def create_service(self, service_name: str, service_version: str, scopes: List[str]):
        creds = await self.db.get(service_name)

        if creds is not None:
            creds = Credentials.from_authorized_user_info(info=json.loads(creds.credentials), scopes=scopes)
        else:
            flow = InstalledAppFlow.from_client_config(settings.google_secret, scopes)
            creds = await self.run_server(flow)
            await self.db.create(service_name=service_name, credentials=str(creds.to_json()))

        if any((creds.valid, creds.expired, creds.refresh_token)):
            creds.refresh(Request())

        return build(service_name, service_version, credentials=creds)

    async def get_values(self, group_index: int) -> Tuple[Any, Any]:
        if group_index == 1:
            starts_with = 7
        else:
            starts_with = 12

        values = self.sheets_service.spreadsheets().values().get(
            spreadsheetId=settings.spreadsheet_original_id,
            majorDimension='COLUMNS',
            range=f"{group_index} курс!D{starts_with}:AD253"
        ).execute()

        hyperlinks_raw = self.sheets_service.spreadsheets().get(
            spreadsheetId=settings.spreadsheet_original_id,
            fields="sheets(data(rowData(values(hyperlink))))",
            ranges=f"{group_index} курс!D{starts_with}:AD253"
        ).execute()
        hyperlinks = hyperlinks_raw.get('sheets')[0].get("data")[0]

        return values, await safe_get_dict(hyperlinks, 'rowData')
