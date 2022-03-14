from config import settings
from refactor.backend.google_api.handlers import GoogleApiHandler

current_spreadsheet = settings.spreadsheet_original_id


def get_spreadsheet_url(spreadsheet_id):
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit#gid=594793772"


class SheetScraper:
    def __init__(self, group_index: int):
        self.group_index = group_index
        self.__range = self.__find_range()
        self.__spreadsheet_id = current_spreadsheet

    async def read_column(self) -> dict:
        if self.__wrong_group_index():
            return {'values': ["invalid index"]}

        google_api = GoogleApiHandler()
        await google_api.init_services()

        response = google_api.sheets_service.spreadsheets().values().get(
            spreadsheetId=self.__spreadsheet_id,
            majorDimension='COLUMNS',
            range=self.__range  # smth like '2 курс!T12:T253'
        ).execute()

        return response

    async def get_links(self) -> dict:

        if self.__wrong_group_index():
            return {'values': ["invalid index"]}

        fields = "sheets(data(rowData(values(hyperlink))))"

        google_api = GoogleApiHandler()
        await google_api.init_services()

        links = google_api.sheets_service.spreadsheets().get(
            spreadsheetId=self.__spreadsheet_id,
            fields=fields,
            ranges=self.__range
        ).execute()['sheets']  # превышение лимита

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


BASE_GRADE = {
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
    '27': 'AD',
}

SECOND_GRADE_BASE = {
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
    '18': 'T',
}

FIRST_GRADE = BASE_GRADE.copy()
SECOND_GRADE = SECOND_GRADE_BASE.copy()
THIRD_GRADE = BASE_GRADE.copy()
FOURTH_GRADE = BASE_GRADE.copy()

FIRST_GRADE['startswith'] = '7'
SECOND_GRADE['startswith'] = '12'
THIRD_GRADE['startswith'] = '12'
FOURTH_GRADE['startswith'] = '12'
FIRST_GRADE['endswith'] = '70'
SECOND_GRADE['endswith'] = '75'
THIRD_GRADE['endswith'] = '75'
FOURTH_GRADE['endswith'] = '75'
