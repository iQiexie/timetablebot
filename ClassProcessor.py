# extracts data from google sheets columns and pretty prints it

from SheetScraper import SheetScraper
import datetime


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


get_time = {
    0: '[09:00 - 10:30]:\n\n',
    1: '[10:40 - 12:10]:\n\n',
    2: '[12:40 - 14:10]:\n\n',
    3: '[14:20 - 15:50]:\n\n',
    4: '[16:00 - 17:30]:\n\n'
}

get_weekday_name = {
    0: 'Понедельник',
    1: 'Вторник',
    2: 'Среда',
    3: 'Четверг',
    4: 'Пятница',
    5: 'Суббота',
    6: 'Воскресенье',
}


class ClassProcessor:
    def __init__(self, group_index: int):
        self.ss = SheetScraper(group_index)
        self.classes = self.ss.read_column()['values'][0]  # столбик с расписанием
        self.links = self.ss.get_links()[0]["data"][0]["rowData"]
        self.weekday = datetime.datetime.today().weekday()  # порядковый номер дня текущей недели

    def get_today(self) -> str:
        return self.getByDay(self.weekday)

    def get_tomorrow(self) -> str:
        return self.getByDay(self.weekday + 1)

    def getByDay(self, week_day_index: int, next_week=False) -> str:

        if self.classes == 'invalid index':
            return "Поменяй группу в настройках"

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

        # проверка на воскресенье
        if week_day_index > 6:
            week_day_index -= 7

        if week_day_index == 6:
            return 'Какие пары? Это воскресенье. Только я тут один 24/7 работаю'

        # выбираем стартовую позицию для курсора
        if isWeekAbove(current_week):
            current_position = 0 + (week_day_index * 40)  # 40 - количество линий, которые занимает день
        else:
            current_position = 4 + (week_day_index * 40)

        outliner = f'({get_weekday_name[week_day_index]}, ' \
                   f'{isWeekAbove_string(current_week)}, ' \
                   f'неделя №{current_week}, ' \
                   f'{today.strftime("%d.%m.%Y")})\n\n'

        text = outliner

        text += self.__format_classes(current_position)

        text += outliner

        return text

    def __format_classes(self, current_position: int) -> str:

        text = ''

        STEP = 4  # количество линий, которые надо пропускать. Именно столько занимает одна пара

        for i in range(5):
            text += get_time[i]

            for current_position in range(current_position, current_position + STEP):
                try:
                    # Пытаемся добавить пару в строку

                    text += self.classes[current_position]
                except IndexError:
                    pass

                try:
                    # пытаемся добавить ссылку к паре в строку

                    text += f'\n\nСсылка: {self.links[current_position]["values"][0]["hyperlink"]}\n'
                except (KeyError, IndexError):
                    pass
                text += '\n'

            current_position += STEP + 1
            text += '\n\n๐৹ₒₒₒₒₒₒₒₒₒₒₒ৹๐\n\n'

        return text
