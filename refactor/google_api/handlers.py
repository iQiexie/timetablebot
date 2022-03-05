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


class GoogleApiHandler:
    def __init__(self, db: GoogleApiCRUD):
        self.db = db
    #
    # @staticmethod
    # def create_google_creds(scopes, service_name, service_version) -> Tuple:
    #
    #     return build(service_name, service_version, credentials=cred), cred

    async def create_service(self, service_name: str, service_version: str, scopes: List[str]):
        # cred = await self.db.get("google")

        aiogoogle = Aiogoogle(service_account_creds=settings.google_secret)
        await aiogoogle.service_account_manager.detect_default_creds_source()


        # if cred is None:
        #     service, cred = self.create_google_creds(scopes, service_name, service_version)
        #     await self.db.create(service_name="google", credentials=str(cred.to_json()))

        # try:
        #     service = build(api_service_name, api_version, credentials=cred)
        #     print(api_service_name, 'service created successfully')
        #     return service
        # except Exception as e:
        #     print('Unable to connect.')
        #     print(e)
        #     return None
