# extracts data from google sheets columns and pretty prints it
from SheetScraper import SheetScraper
import datetime


def isWeekAbove():
    # проверяет, идёт ли сейчас неделя над линией
    # если неделя нечётная, то она над линией
    # если неделя чётная, то она под линией

    return datetime.date.today().isocalendar()[1] % 2 != 0


def get_time():
    return {
        0: '[09:00 - 10:30]:\n\n',
        1: '[10:40 - 12:10]:\n\n',
        2: '[12:40 - 14:10]:\n\n',
        3: '[14:20 - 15:50]:\n\n',
        4: '[16:00 - 17:30]:\n\n'
    }


class ClassProcessor:
    def __init__(self, group_index):
        self.SS = SheetScraper(group_index)
        self.classes = self.SS.read_column()['values'][0]

    def getByDay(self, week_day_index):
        # week_day_index - порядковый номер дня недели, начиная с 0. Понедельник - 0, воскресенье - 6.

        # выбираем стартовую позицию для курсора
        if isWeekAbove():
            current_position = 0 + (week_day_index * 40)  # 40 - количество линий, которые занимает день
        else:
            current_position = 4 + (week_day_index * 40)

        # количество линий, которые надо пропускать. Именно столько занимает одна пара
        step_const = 4
        text = ''

        for i in range(5):
            text += get_time()[i]

            for current_position in range(current_position, current_position + step_const):
                text += self.classes[current_position]

            current_position += step_const + 1
            text += '\n\n๐৹ₒₒₒₒₒₒₒₒₒₒₒ৹๐'
            text += '\n\n'

        return text
