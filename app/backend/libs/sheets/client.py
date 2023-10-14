import json
from typing import Any
from typing import List

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from app.backend.db.repos.credentials import CredentialsRepo
from app.backend.libs.dto.sheets import Sheet
from app.backend.libs.sheets.flow import InstalledAppFlow
from config import settings

# TODO refactor


class GoogleAPI:
    def __init__(self, repo: CredentialsRepo):
        self.repo = repo
        self.sheets_service = None

    async def init_services(self) -> None:
        self.sheets_service = await self.create_service(
            service_name="sheets",
            service_version="v4",
            scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"],
        )

    async def create_service(
        self,
        service_name: str,
        service_version: str,
        scopes: List[str],
    ) -> Any:
        creds = await self.repo.get_credentials(service_name=service_name)

        if creds is not None:
            creds = Credentials.from_authorized_user_info(
                info=json.loads(creds.credentials),
                scopes=scopes,
            )
        else:
            flow = InstalledAppFlow.from_client_config(
                client_config=settings.GOOGLE_SECRET,
                scopes=scopes,
            )
            creds = flow.run_local_server(host="localhost", port=1234)
            await self.repo.create_credentials(
                service_name=service_name,
                credentials=str(creds.to_json()),
            )

        if any((creds.valid, creds.expired, creds.refresh_token)):
            creds.refresh(Request())

        return build(service_name, service_version, credentials=creds)

    async def read_sheet(self, group_index: int) -> Sheet:
        if self.sheets_service is None:
            raise RuntimeError("Sheets service is not initialized")

        range_str = f"{group_index} курс"  # literal sheet's name

        values = (
            self.sheets_service.spreadsheets()
            .get(
                spreadsheetId=settings.SPREADSHEET_ID,
                fields="sheets/data/rowData/values(hyperlink,formattedValue,textFormatRuns/format/link/uri)",  # noqa
                ranges=range_str,
            )
            .execute()
        )

        sheet = Sheet.parse_obj(values["sheets"][0]["data"][0])
        return sheet
