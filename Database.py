import os
import sqlite3

import os
import sqlite3


class Database:
    def __init__(self, user):
        # user - peer_id

        self.__user = user
        self.__path = f"{os.path.dirname(__file__)}\\Database\\USERS\\{self.__user}.db"

        if os.path.isfile(self.__path):
            pass
        else:
            self.create_db()

    def create_db(self):
        self.__cursor_execute(f"""CREATE TABLE IF NOT EXISTS general (
                                    group_index INT UNIQUE PRIMARY KEY
                                    )""")
        self.__cursor_execute(f'INSERT INTO general VALUES (1)')

    def update_group_index(self, index):

        self.__cursor_execute(f"""UPDATE general
                                SET group_index = {index}
                                WHERE
                                    ROWID = 1""")

    def get_group_index(self):
        unformatted_list = self.__cursor_fetchall(f"""SELECT group_index FROM general""")

        return unformatted_list[0][0]

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
