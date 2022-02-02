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
SPREADSHEETID = '1xrrFFR1pnfwECCe5cFOe02QSW5VhtvdiLCyC7ehlUJg'