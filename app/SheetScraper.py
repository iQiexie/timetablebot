import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from Assets.Strings import current_spreadsheet
from config import SPREADSHEETID, SECOND_GRADE, FIRST_GRADE, THIRD_GRADE, FOURTH_GRADE


def Create_Service(client_secret_file, api_service_name, api_version, scopes):
    cred = None

    creds_file = f'secret/token_{api_service_name}_{api_version}.json'

    if os.path.exists(creds_file):
        cred = Credentials.from_authorized_user_file(filename=creds_file, scopes=scopes)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
            cred = flow.run_local_server()

        with open(creds_file, 'w') as token:
            token.write(str(cred.to_json()))

    try:
        service = build(api_service_name, api_version, credentials=cred)
        print(api_service_name, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


sheets_service = Create_Service(
    'secret/secret.json',
    'sheets',
    'v4',
    ['https://www.googleapis.com/auth/spreadsheets.readonly']
)

drive_service = Create_Service(
    'secret/secret.json',
    'drive',
    'v2',
    ['https://www.googleapis.com/auth/drive']
)


def get_spreadsheet_url(spreadsheet_id):
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid=594793772"


def delete_spreadsheet(spreadsheet_id):
    drive_service.files().delete(
        fileId=spreadsheet_id
    ).execute()

    print("Deleted:", get_spreadsheet_url(spreadsheet_id))


def update_spreadsheet():
    new_spreadsheet = drive_service.files().copy(
        fileId=SPREADSHEETID,
        convert=True
    ).execute()

    print("Created:", get_spreadsheet_url(new_spreadsheet['id']))

    return new_spreadsheet['id']


class SheetScraper:
    def __init__(self, group_index: int):
        self.group_index = group_index
        self.__range = self.__find_range()
        self.__spreadsheet_id = current_spreadsheet['id']

    def read_column(self) -> dict:

        if self.__wrong_group_index():
            return {'values': ["invalid index"]}

        response = sheets_service.spreadsheets().values().get(
            spreadsheetId=self.__spreadsheet_id,
            majorDimension='COLUMNS',
            range=self.__range  # smth like '2 курс!T12:T253'
        ).execute()

        return response

    def get_links(self) -> dict:

        if self.__wrong_group_index():
            return {'values': ["invalid index"]}

        fields = "sheets(data(rowData(values(hyperlink))))"

        links = sheets_service.spreadsheets().get(spreadsheetId=self.__spreadsheet_id,
                                                  fields=fields,
                                                  ranges=self.__range).execute()['sheets']  # превышение лимита

        return links

    def __wrong_group_index(self):
        if self.group_index < 101:
            return True
        else:
            return False

    def __find_range(self) -> str:

        if self.__wrong_group_index():
            return ''

        grade = str(self.group_index)[:1]
        group_subindex = str(self.group_index)[1:]

        if grade == '1':
            first_range = FIRST_GRADE[str(group_subindex)] + FIRST_GRADE['startswith']
            second_range = FIRST_GRADE[str(group_subindex)] + FIRST_GRADE['endswith']

        elif grade == '2':
            first_range = SECOND_GRADE[str(group_subindex)] + SECOND_GRADE['startswith']
            second_range = SECOND_GRADE[str(group_subindex)] + SECOND_GRADE['endswith']

        elif grade == '3':
            first_range = THIRD_GRADE[str(group_subindex)] + THIRD_GRADE['startswith']
            second_range = THIRD_GRADE[str(group_subindex)] + THIRD_GRADE['endswith']

        else:
            first_range = FOURTH_GRADE[str(group_subindex)] + FOURTH_GRADE['startswith']
            second_range = FOURTH_GRADE[str(group_subindex)] + FOURTH_GRADE['endswith']

        return f"{grade} КУРС!{first_range}:{second_range}"
