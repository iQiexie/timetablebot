import asyncio

from aiogoogle import Aiogoogle
from aiogoogle.auth.utils import create_secret

from config import settings

EMAIL = "example@gmail.com"
secret = settings.google_secret.get("installed")
CLIENT_CREDS = {
    "client_id": secret.get("client_id"),
    "client_secret": secret.get("client_secret"),
    "scopes": ['https://www.googleapis.com/auth/spreadsheets.readonly', 'https://www.googleapis.com/auth/drive'],
    "redirect_uri": "http://localhost"
}

state = create_secret()  # Shouldn't be a global hardcoded variable.
LOCAL_ADDRESS = "localhost"
LOCAL_PORT = "5000"
aiogoogle = Aiogoogle(client_creds=CLIENT_CREDS)


async def authorize():
    if aiogoogle.oauth2.is_ready(CLIENT_CREDS):
        uri = aiogoogle.oauth2.authorization_url(
            client_creds=CLIENT_CREDS,
            state=state,
            access_type="offline",
            include_granted_scopes=True,
            login_hint=EMAIL,
            prompt="select_account",
        )

    # full_user_creds = await aiogoogle.oauth2.build_user_creds(
    #     grant=uri.get("code"), client_creds=CLIENT_CREDS
    # )


asyncio.run(authorize())
