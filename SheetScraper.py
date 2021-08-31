import pickle
import os

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


# -- Google library --

CLIENT_SECRET_FILE = 'secret/secret.json'
API_SERVICE_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']


def Create_Service():
    cred = None

    pickle_file = f'secret/token_{API_SERVICE_NAME}_{API_VERSION}.pickle'

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


# -- Google library --

service = Create_Service()


class SheetScraper:
    def __init__(self, group_index: int):
        self.group_index = group_index

        self.__grade = str(group_index)[:1]
        self.__group_subindex = str(group_index)[1:]
        self.__range = self.__find_range()

        with open('Assets/spreadsheet_id', 'r') as f:
            self.__spreadsheet_id = f.read()

    def read_column(self) -> dict:

        if self.group_index == 1:  # если номер группы стандартный (см. Database.create_db())
            return {'values': ["invalid index"]}

        response = service.spreadsheets().values().get(
            spreadsheetId=self.__spreadsheet_id,
            majorDimension='COLUMNS',
            range=self.__range  # smth like '2 курс!T12:T253'
        ).execute()

        return response

    def get_links(self) -> dict:
        if self.group_index == 1:  # если номер группы стандартный (см. Database.create_db())
            return {'values': ["invalid index"]}

        fields = "sheets(data(rowData(values(hyperlink))))"

        links = service.spreadsheets().get(spreadsheetId=self.__spreadsheet_id,
                                         fields=fields,
                                         ranges=self.__range).execute()['sheets']

        return links

    def __find_range(self) -> str:

        if self.group_index == 1:  # если номер группы стандартный (см. Database.create_db())
            return {'values': ["invalid index"]}

        first_grade = {
            '01': 'D',
            '02': 'E',
            '03': 'F',
            '04': 'G',
            '05': 'H',
            '06': 'I',
            '07': 'G',
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

        second_grade = {
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

        third_grade = {
            '01': 'D',
            '02': 'E',
            '03': 'F',
            '04': 'G',
            '05': 'H',
            '06': 'I',
            '07': 'G',
            '08': 'K',
            '09': 'L',
            '10': 'M',
            '11': 'N',
            '12': 'O',
            '13': 'P',
            '14': 'Q',
            '15': 'R',
            '16': 'S',
            '17': 'T'
        }

        fourth_grade = {
            '01': 'D',
            '02': 'E',
            '03': 'F',
            '04': 'G',
            '05': 'H',
            '06': 'I',
            '07': 'G',
            '08': 'K',
            '09': 'L',
            '10': 'M',
            '11': 'N',
        }

        first_range = ''
        second_range = ''

        if self.__grade == '1':
            first_range = first_grade[str(self.__group_subindex)] + "13"
            second_range = first_grade[str(self.__group_subindex)] + "253"

        elif self.__grade == '2':
            first_range = second_grade[str(self.__group_subindex)] + "13"
            second_range = second_grade[str(self.__group_subindex)] + "253"

        elif self.__grade == '3':
            first_range = third_grade[str(self.__group_subindex)] + "13"
            second_range = third_grade[str(self.__group_subindex)] + "253"

        elif self.__grade == '4':
            first_range = fourth_grade[str(self.__group_subindex)] + "13"
            second_range = fourth_grade[str(self.__group_subindex)] + "253"

        text = f"{self.__grade} курс!{first_range}:{second_range}"

        return text
