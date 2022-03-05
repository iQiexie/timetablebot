import json
from contextlib import contextmanager
from typing import List, Tuple
import asyncio

from aiogoogle import Aiogoogle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import settings
from refactor.google_api.crud import GoogleApiCRUD
from refactor.google_api.schemas import CredentialSchema


class GoogleApiHandler:
    def __init__(self, db: GoogleApiCRUD):
        self.db = db

    @staticmethod
    async def server(flow):
        return flow.run_local_server()

    async def create_service(self, service_name: str, service_version: str, scopes: List[str]):
        creds = await self.db.get("google")

        if creds is not None:
            creds = Credentials.from_authorized_user_info(info=json.loads(creds.credentials), scopes=scopes)
        else:
            flow = InstalledAppFlow.from_client_config(settings.google_secret, scopes)
            creds = await self.server(flow)
            await self.db.create(service_name="google", credentials=str(creds.to_json()))

        if any((creds.valid, creds.expired, creds.refresh_token)):
            creds.refresh(Request())

        return build(service_name, service_version, credentials=creds)
