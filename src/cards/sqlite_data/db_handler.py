import os
import sqlite3
from .utils import CREATE_DB_QUERY


class SqliteDbHandler:
    def __init__(self, db_path):
        self.db_path = db_path

    def initialize_db(self, init_db_query=CREATE_DB_QUERY):
        if os.path.exists(self.db_path):
            self.delete_database_file()

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.executescript(init_db_query)
        conn.commit()
        conn.close()

    def list_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        tables = cursor.fetchall()
        conn.close()

        return [table[0] for table in tables]

    def clear_database_data(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = OFF;")
        conn.commit()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table_name in tables:
            cursor.execute(f'DELETE FROM {table_name[0]}')

        cursor.execute("PRAGMA foreign_keys = ON;")
        conn.commit()
        conn.close()

    def delete_all_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("PRAGMA foreign_keys = OFF;")
        conn.commit()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table_name in tables:
            cursor.execute(f'DROP TABLE IF EXISTS {table_name[0]}')

        cursor.execute("PRAGMA foreign_keys = ON;")
        conn.commit()
        conn.close()

    def delete_database_file(self):
        os.remove(self.db_path)
