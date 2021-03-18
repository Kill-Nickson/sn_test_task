from os.path import exists
import sqlite3


class Database:

    def __init__(self, path='./databases/bots.db'):
        self.db_path = path

    def _table_init(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(""" CREATE TABLE IF NOT EXISTS matches (
                                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        email TEXT NOT NULL,
                                                        password TEXT NOT NULL
                                                        )""")
                conn.commit()
        except Exception as e:
            print('An error occurred:', e)

    def table_update(self, bots):
        if not exists(self.db_path):
            self._table_init()
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.executemany("INSERT INTO matches(email,password) VALUES (?,?)", bots)
                conn.commit()
        except Exception as e:
            print('An error occurred:', e)
