import os
import pickle

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# -- Google library --

def Create_Service(client_secret_file, api_service_name, api_version, scopes):
    cred = None

    pickle_file = f'secret/token_{api_service_name}_{api_version}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, scopes)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(api_service_name, api_version, credentials=cred)
        print(api_service_name, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


# -- Google library --

sheets_service = Create_Service('secret/secret.json',
                                'sheets',
                                'v4',
                                ['https://www.googleapis.com/auth/spreadsheets.readonly'])

drive_service = Create_Service('secret/secret.json',
                               'drive',
                               'v2',
                               ['https://www.googleapis.com/auth/drive'])


def update_spreadsheet():
    new_spreadsheet = drive_service.files().copy(
        fileId="1_opvVKnFlMR_jZEuohoVczocRf__Icem",
        convert=True
    ).execute()

    print("Spreadsheet updated")

    return new_spreadsheet['id']


class SheetScraper:
    def __init__(self, group_index: int):
        self.group_index = group_index
        self.__range = self.__find_range()

        with open('Assets/spreadsheet_id', 'r') as f:
            self.__spreadsheet_id = f.readline()

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
                                                  ranges=self.__range).execute()['sheets']

        return links

    def __wrong_group_index(self):
        if self.group_index < 101:
            return True
        else:
            return False

    def __find_range(self) -> str:

        if self.__wrong_group_index():
            return ''

        FIRST_GRADE = {
            '01': 'D',
            '02': 'E',
            '03': 'F',
            '04': 'G',
            '05': 'H',
            '06': 'I',
            '07': 'J',
            '08': 'K',
            '09': 'L',
            '10': 'M',
            '11': 'N',
            '12': 'O',
            '13': 'P',
            '14': 'Q',
            '15': 'R',
            '16': 'S',
            '17': 'T',
            '18': 'U',
            '19': 'V',
            '20': 'W',
            '21': 'X',
            '22': 'Y',
            '23': 'Z',
            '24': 'AA',
            '25': 'AB',
            '26': 'AC',
            '27': 'AD'
        }

        SECOND_GRADE = {
            '01': 'D',
            '02': 'E',
            '03': 'F',
            '04': 'G',
            '05': 'H',
            '06': 'I',
            '07': 'G',
            '08': 'K',
            '09': 'L',
            '11': 'M',
            '12': 'N',
            '13': 'O',
            '14': 'P',
            '15': 'Q',
            '16': 'R',
            '17': 'S',
            '18': 'T'
        }

        grade = str(self.group_index)[:1]
        group_subindex = str(self.group_index)[1:]

        if grade == '2':
            first_range = SECOND_GRADE[str(group_subindex)] + "13"
            second_range = SECOND_GRADE[str(group_subindex)] + "253"

        elif grade == '1':
            first_range = FIRST_GRADE[str(group_subindex)] + "15"
            second_range = FIRST_GRADE[str(group_subindex)] + "300"

        else:
            first_range = FIRST_GRADE[str(group_subindex)] + "13"
            second_range = FIRST_GRADE[str(group_subindex)] + "253"

        return f"{grade} курс!{first_range}:{second_range}"
