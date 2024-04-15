import sqlite3
import random
import string


def generate_unique_id(db_path, table_name, column_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    while True:
        new_id = ''.join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )
        query = f"""
            SELECT EXISTS(SELECT 1 FROM {table_name} WHERE {column_name}=?)
        """
        cursor.execute(query, (new_id,))
        exists = cursor.fetchone()[0]
        if not exists:
            break

    conn.close()
    return new_id


CREATE_DB_QUERY = """
    CREATE TABLE IF NOT EXISTS CardsStatus (
        status TEXT,
        CONSTRAINT status_check CHECK (status IN ('present', 'absent'))
    );

    INSERT INTO CardsStatus (status) VALUES ('present'), ('absent');

    CREATE TABLE IF NOT EXISTS Cardset (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        created_at DATETIME NOT NULL,
        modified_at DATETIME NOT NULL,
        addressed_at DATETIME,
        status TEXT NOT NULL,
        owner_id TEXT NOT NULL,
        FOREIGN KEY (status) REFERENCES CardsStatus(status)
    );

    CREATE TABLE IF NOT EXISTS Card (
        id TEXT PRIMARY KEY,
        term TEXT NOT NULL,
        description TEXT,
        created_at DATETIME NOT NULL,
        modified_at DATETIME NOT NULL,
        addressed_at DATETIME,
        status TEXT NOT NULL,
        owner_id TEXT NOT NULL,
        cardset_id TEXT NOT NULL,
        FOREIGN KEY (status) REFERENCES CardsStatus(status),
        FOREIGN KEY (cardset_id) REFERENCES Cardset(id) ON DELETE CASCADE
    );
"""
