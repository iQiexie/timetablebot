import os
import sqlite3


class Database:
    def __init__(self, user):
        # user - peer_id

        self.__user = user
        self.__path = f"{os.path.dirname(__file__)}/DATABASE/USERS/{self.__user}.db"

        self.first_message = False

        if os.path.isfile(self.__path):
            pass
        else:
            self.first_message = True
            self.create_db()

        if self.__ai_table_exists():
            # Создаём табличку с настройками ии, если её не существует
            pass

    def create_db(self):
        self.__cursor_execute("""CREATE TABLE IF NOT EXISTS general (
                                    group_index INT UNIQUE PRIMARY KEY
                                    )""")
        self.__cursor_execute('INSERT INTO general VALUES (1)')

    def update_group_index(self, index):

        self.__cursor_execute(f"""UPDATE general
                                SET group_index = {index}
                                WHERE
                                    ROWID = 1""")

    def get_group_index(self):
        unformatted_list = self.__cursor_fetchall("SELECT group_index FROM general")
        return unformatted_list[0][0]

    def update_ai(self, state):
        # 0 - off, 1 - on
        if self.__ai_table_exists():
            self.__cursor_execute(f"""UPDATE ai
                                    SET enabled = {state}
                                    WHERE
                                        ROWID = 1""")

    def get_ai(self):
        unformatted_list = self.__cursor_fetchall("SELECT enabled FROM ai")
        if len(unformatted_list) > 0:
            return unformatted_list[0][0]
        else:
            return None

    def __ai_table_exists(self):
        self.__cursor_execute("""CREATE TABLE IF NOT EXISTS ai (
                                enabled INT UNIQUE PRIMARY KEY
                                )""")
        if self.get_ai() == 1 or self.get_ai() == 0:
            return True
        else:
            self.__cursor_execute(f'INSERT INTO ai VALUES (0)')
            return False

    def __cursor_execute(self, command):
        database = sqlite3.connect(self.__path)
        cursor = database.cursor()

        cursor.execute(command)

        database.commit()
        database.close()

    def __cursor_fetchall(self, command):
        database = sqlite3.connect(self.__path)
        cursor = database.cursor()

        cursor.execute(command)
        result = cursor.fetchall()

        database.commit()
        database.close()

        return result
