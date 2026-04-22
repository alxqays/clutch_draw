import sqlite3


class Database:
    def __init__(self):
        pass

    def insert_account(self, username: str, password: str) -> None:
        # 1. Connect to a database (creates it if it doesn't exist)
        conn = sqlite3.connect("clutch_draw.db")

        # 2. Create a cursor (used to run SQL commands)
        cursor = conn.cursor()

        # 3. Create a table
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS accounts (
            username PRIMARY KEY,
            password TEXT,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0
        )
        """
        )

        # 4. Insert data
        cursor.execute(
            "INSERT INTO accounts (username, password) VALUES (?, ?)",
            (username, password),
        )

        # 5. Save changes
        conn.commit()

        # 7. Close connection
        conn.close()

    def account_exists(self, username: str) -> bool:
        # 1. Connect to a database (creates it if it doesn't exist)
        conn = sqlite3.connect("clutch_draw.db")

        # 2. Create a cursor (used to run SQL commands)
        cursor = conn.cursor()

        # 3. Read data
        cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
        account = cursor.fetchone()

        # 4. Close connection
        conn.close()

        if account is None:
            return False
        else:
            return True

    def fetch_accounts(self) -> list[tuple[str, str]]:
        # 1. Connect to a database (creates it if it doesn't exist)
        conn = sqlite3.connect("clutch_draw.db")

        # 2. Create a cursor (used to run SQL commands)
        cursor = conn.cursor()

        # 3. Read data
        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()  # list[tuple[int, str, str]]

        # 4. Close connection
        conn.close()

        return accounts

    def get_account(self, username: str) -> tuple[str, str] | None:
        # 1. Connect to a database (creates it if it doesn't exist)
        conn = sqlite3.connect("clutch_draw.db")

        # 2. Create a cursor (used to run SQL commands)
        cursor = conn.cursor()

        # 3. Read data
        cursor.execute(
            "SELECT username, password, xp, level, wins, losses FROM accounts WHERE username = ?",
            (username,),
        )
        account = cursor.fetchone()  # tuple[int, str, str] | None

        # 4. Close connection
        conn.close()

        return account

    def update_account(self, username, xp, level, wins, losses):
        conn = sqlite3.connect("clutch_draw.db")
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE accounts
            SET xp = ?, level = ?, wins = ?, losses = ?
            WHERE username = ?
            """,
            (xp, level, wins, losses, username),
        )

        conn.commit()
        conn.close()
