import json
from random import randint
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import settings
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

    async def update_sheet(self):
        await self.db.logger.create_log(data="created reger")
        # if settings.spreadsheet_current_id is not None:
        #     self.drive_service.files().delete(fileId=settings.spreadsheet_current_id).execute()

        # new = self.drive_service.files().copy(fileId=settings.spreadsheet_original_id, convert=True).execute()
