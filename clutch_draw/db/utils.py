import sqlite3


class Database:

    def __init__(self):
        pass  # Nothing is initialised here as a new database connection is made in each method

    def insert_account(self, username: str, password: str) -> None:

        # Connecting to the database (it will be created if it doesn't already exist)
        conn = sqlite3.connect("clutch_draw.db")

        # Creating a cursor so that SQL commands can be run
        cursor = conn.cursor()

        # Creating the accounts table if it doesn't already exist
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS accounts (
            username TEXT PRIMARY KEY,
            password TEXT,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            wins INTEGER DEFAULT 0,
            losses INTEGER DEFAULT 0
        )
        """
        )

        # Inserting a new account into the table
        cursor.execute(
            "INSERT INTO accounts (username, password) VALUES (?, ?)",  # "?" act as placeholders so that values can be inserted safely
            (username, password),
        )

        # Saves the changes made
        conn.commit()

        # Closes the connection
        conn.close()

    def account_exists(self, username: str) -> bool:

        # Connecting to the database (it will be created if it doesn't already exist)
        conn = sqlite3.connect("clutch_draw.db")

        # Creating a cursor so that SQL commands can be run
        cursor = conn.cursor()

        # Checks if a username already exists
        cursor.execute("SELECT * FROM accounts WHERE username = ?", (username,))
        account = cursor.fetchone()

        # Closes the connection
        conn.close()

        # If nothing is found, return False, otherwise return True
        if account is None:
            return False
        else:
            return True

    def fetch_accounts(self) -> list[tuple[str, str, int, int, int, int]]:

        # Connecting to the database (it will be created if it doesn't already exist)
        conn = sqlite3.connect("clutch_draw.db")

        # Creating a cursor so that SQL commands can be run
        cursor = conn.cursor()

        # Gets all the accounts from the table
        cursor.execute("SELECT * FROM accounts")
        accounts = cursor.fetchall()

        # Closes the connection
        conn.close()

        # Returns all account data
        return accounts

    def get_account(self, username: str) -> tuple[str, str, int, int, int, int] | None:

        # Connecting to the database (it will be created if it doesn't already exist)
        conn = sqlite3.connect("clutch_draw.db")

        # Creating a cursor so that SQL commands can be run
        cursor = conn.cursor()

        # Gets one specific account using the account's username
        cursor.execute(
            "SELECT username, password, xp, level, wins, losses FROM accounts WHERE username = ?",
            (username,),
        )
        account = cursor.fetchone()

        # Closes the connection
        conn.close()

        return account

    def update_account(
        self, username: str, xp: int, level: int, wins: int, losses: int
    ) -> None:

        # Connecting to the database (it will be created if it doesn't already exist)
        conn = sqlite3.connect("clutch_draw.db")

        # Creating a cursor so that SQL commands can be run
        cursor = conn.cursor()

        # Updating the user's stats: XP, Level, Wins, Losses
        cursor.execute(
            """
            UPDATE accounts
            SET xp = ?, level = ?, wins = ?, losses = ?
            WHERE username = ?
            """,
            (xp, level, wins, losses, username),
        )

        # Saves the changes made
        conn.commit()

        # Closes the connection
        conn.close()
