# extracts data from google sheets columns and pretty prints it
from SheetScraper import SheetScraper
import datetime


def isWeekAbove():
    # проверяет, идёт ли сейчас неделя над линией
    # если неделя нечётная, то она над линией
    # если неделя чётная, то она под линией

    return datetime.date.today().isocalendar()[1] % 2 != 0


def isWeekAbove_string():
    if isWeekAbove():
        return 'над чертой'
    else:
        return 'под чертой'


def get_time():
    return {
        0: '[09:00 - 10:30]:\n\n',
        1: '[10:40 - 12:10]:\n\n',
        2: '[12:40 - 14:10]:\n\n',
        3: '[14:20 - 15:50]:\n\n',
        4: '[16:00 - 17:30]:\n\n'
    }


def get_weekday_name():
    return {
        0: 'Понедельник',
        1: 'Вторник',
        2: 'Среда',
        3: 'Четверг',
        4: 'Пятница',
        5: 'Суббота',
        6: 'Воскресенье',
    }


def get_weekday_index():
    # метод для получение порядкового номера дня недели в main.py

    return datetime.datetime.today().weekday()


class ClassProcessor:
    def __init__(self, group_index):
        self.SS = SheetScraper(group_index)
        self.classes = self.SS.read_column()['values'][0]  # список из полей листа
        self.weekday = datetime.datetime.today().weekday()  # порядковый номер текущей недели

    def get_today(self):
        return self.getByDay(self.weekday)

    def get_tomorrow(self):
        return self.getByDay(self.weekday + 1)

    def getByDay(self, week_day_index):
        # week_day_index - порядковый номер дня недели, начиная с 0. Понедельник - 0, воскресенье - 6.
        # timedelta = сколько дней нужно добавить к текущей дате

        timedelta = week_day_index - self.weekday
        today = (datetime.date.today() + datetime.timedelta(days=timedelta))

        if week_day_index > 6:
            week_day_index -= 7

        # проверка на воскресенье
        if week_day_index == 6:
            return 'Какие пары? Это воскресенье. Это только я тут 24/7 работаю'

        # выбираем стартовую позицию для курсора
        if isWeekAbove():
            current_position = 0 + (week_day_index * 40)  # 40 - количество линий, которые занимает день
        else:
            current_position = 4 + (week_day_index * 40)

        step_const = 4  # количество линий, которые надо пропускать. Именно столько занимает одна пара

        text = f'({get_weekday_name()[week_day_index]}, ' \
               f'{isWeekAbove_string()}, ' \
               f'неделя №{today.isocalendar()[1]}, ' \
               f'{today.strftime("%d.%m.%Y")})\n\n'

        for i in range(5):
            text += get_time()[i]

            for current_position in range(current_position, current_position + step_const):
                try:
                    text += self.classes[current_position]
                except IndexError:
                    pass
                text += '\n'

            current_position += step_const + 1
            text += '\n\n๐৹ₒₒₒₒₒₒₒₒₒₒₒ৹๐'
            text += '\n\n'

        return text
