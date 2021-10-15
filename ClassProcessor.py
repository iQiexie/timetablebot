# extracts data from google sheets columns and pretty prints it

from SheetScraper import SheetScraper
import datetime

GET_TIME: dict = {
    0: '[09:00 - 10:30]:\n\n',
    1: '[10:40 - 12:10]:\n\n',
    2: '[12:40 - 14:10]:\n\n',
    3: '[14:20 - 15:50]:\n\n',
    4: '[16:00 - 17:30]:\n\n'
}

GET_WEEKDAY_NAME: dict = {
    0: 'Понедельник',
    1: 'Вторник',
    2: 'Среда',
    3: 'Четверг',
    4: 'Пятница',
    5: 'Суббота',
    6: 'Воскресенье',
}

INVALID_INDEX_MESSAGE: str = 'Поменяй группу в настройках. Для этого напиши "старт", а потом нажми на "настройки"'
SUNDAY_MESSAGE: str = 'Какие пары? Это воскресенье. Только я тут один 24/7 работаю'


def isWeekAbove(week: int) -> bool:
    # проверяет, идёт ли сейчас неделя над линией
    # если неделя нечётная, то она над линией
    # если неделя чётная, то она под линией

    return week % 2 != 0


def isWeekAbove_string(week: int) -> str:
    if isWeekAbove(week):
        return 'над чертой'
    else:
        return 'под чертой'


class ClassProcessor:
    def __init__(self, group_index: int):
        ss = SheetScraper(group_index)
        self.classes = ss.read_column()['values'][0]  # столбик с расписанием
        self.links = ss.get_links()
        self.weekday = datetime.datetime.today().weekday()  # порядковый номер дня текущей недели

    def get_today(self) -> str:
        return self.getByDay(self.weekday)

    def get_tomorrow(self) -> str:
        return self.getByDay(self.weekday + 1)

    def getByDay(self, week_day_index: int, next_week=False) -> str:

        if self.classes == 'invalid index':
            return INVALID_INDEX_MESSAGE

        if next_week:
            timedelta = (week_day_index - self.weekday) + 7
        else:
            timedelta = week_day_index - self.weekday

        return self.__getByDay(week_day_index, timedelta)

    def __getByDay(self, week_day_index: int, timedelta: int) -> str:
        # week_day_index - порядковый номер дня недели, начиная с 0. Понедельник - 0, воскресенье - 6.
        # timedelta = сколько дней нужно добавить к текущей дате

        today = (datetime.date.today() + datetime.timedelta(days=timedelta))
        current_week = today.isocalendar()[1]

        # валидатор дня недели
        if week_day_index > 6:
            week_day_index -= 7

        if week_day_index == 6:
            return SUNDAY_MESSAGE

        # выбираем стартовую позицию для курсора
        if isWeekAbove(current_week):
            current_position = 0 + (week_day_index * 40)  # 40 - количество линий, которые занимает день
        else:
            current_position = 4 + (week_day_index * 40)

        outline = f'({GET_WEEKDAY_NAME[week_day_index]}, ' \
                  f'{isWeekAbove_string(current_week)}, ' \
                  f'неделя №{current_week}, ' \
                  f'{today.strftime("%d.%m.%Y")})\n\n'

        return outline + self.__format_classes(current_position) + outline

    def __format_classes(self, current_position: int) -> str:
        STEP = 4  # количество линий, которые надо пропускать. Именно столько занимает одна пара

        text = ''

        for i in range(5):
            # итерируем пары

            text += GET_TIME[i]  # время пары типа "[09:00 - 10:30]"

            for current_position in range(current_position, current_position + STEP):
                try:
                    # Пытаемся текст ячейки пары в строку (пара состоит из 4 ячеек)
                    text += self.classes[current_position]
                except IndexError:
                    pass

                try:
                    # пытаемся добавить гипер ссылку из ячейки в строку
                    text += f'\n\nСсылка: {self.links[0]["data"][0]["rowData"][current_position]["values"][0]["hyperlink"]}\n'
                except (KeyError, IndexError):
                    pass

                text += '\n'

            current_position += STEP + 1  # переходим к следующей паре
            text += '\n\n\n\n'
            # text += '\n\n๐৹ₒₒₒₒₒₒₒₒₒₒₒ৹๐\n\n'

        return text
