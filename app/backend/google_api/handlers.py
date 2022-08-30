import json
from typing import List, Tuple, Any

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import settings
from app.backend.google_api.crud import GoogleApiREDIS
from app.utils import safe_get_dict


class GoogleApiHandler:
    def __init__(self):
        self.redis = GoogleApiREDIS()
        self.drive_service = None
        self.sheets_service = None

    async def init_services(self):
        """ Обязательно нужно вызывать после каждой инициализации этого круда """

        self.sheets_service = await self.create_service(
            service_name='sheets',
            service_version='v4',
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )

    async def update_credentials(self):
        await self.redis.reset_database()
        await self.init_services()

    async def create_service(self, service_name: str, service_version: str, scopes: List[str]):
        creds = await self.redis.get(service_name)

        if creds is not None:
            creds = Credentials.from_authorized_user_info(info=json.loads(creds), scopes=scopes)
        else:
            flow = InstalledAppFlow.from_client_config(
                settings.google_secret,
                scopes,
            )
            creds = flow.run_local_server(host='localhost', port=1234)
            await self.redis.create(service_name=service_name, credentials=str(creds.to_json()))

        if any((creds.valid, creds.expired, creds.refresh_token)):
            creds.refresh(Request())

        return build(service_name, service_version, credentials=creds)

    async def get_values(self, group_index: int) -> Tuple[Any, Any] | None:
        if self.sheets_service is None:
            return None

        starts_with = 7

        if group_index != 3:
            range_str = f"{group_index} курс!D{starts_with}:AE68"
        else:
            range_str = f"{group_index} курс !D{starts_with}:AE68"

        values = self.sheets_service.spreadsheets().values().get(
            spreadsheetId=settings.spreadsheet_original_id,
            majorDimension='COLUMNS',
            range=range_str
        ).execute()

        hyperlinks_raw = self.sheets_service.spreadsheets().get(
            spreadsheetId=settings.spreadsheet_original_id,
            fields="sheets(data(rowData(values(hyperlink))))",
            ranges=range_str
        ).execute()
        hyperlinks = hyperlinks_raw.get('sheets')[0].get("data")[0]

        return values, await safe_get_dict(hyperlinks, 'rowData')
