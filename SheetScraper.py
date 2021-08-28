import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import datetime


# -- Google library --

def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]

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


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt


# -- Google library --


CLIENT_SECRET_FILE = 'secret/secret.json'
API_NAME = 'sheets'
API_VERSION = 'v4'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


class SheetScraper:
    def __init__(self, group_index):
        self.group_index = group_index

        self.__spreadsheet_id = open("Assets/spreadsheet_id.txt", "r").read()
        self.__grade = str(group_index)[:1]
        self.__group_subindex = str(group_index)[1:]
        self.group_index = group_index

    def read_column(self):

        if self.group_index == 1:
            return {'values': ["invalid index"]}

        _range = self.__find_range()

        response = service.spreadsheets().values().get(
            spreadsheetId=self.__spreadsheet_id,
            majorDimension='COLUMNS',
            range=_range  # smth like '2 курс!T12:T253'
        ).execute()

        return response

    def __find_range(self):
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
            first_range = first_grade[str(self.__group_subindex)] + "12"
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
