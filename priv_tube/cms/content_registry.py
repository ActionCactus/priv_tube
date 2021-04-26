from abc import ABC, abstractmethod
import sqlite3


class RegistryNotInitializedException(Exception):
    pass


class ContentRegistry(ABC):
    """
    A stupid proof-of-concept registry to see if I can read files on the system, seed them in to a
    SQLite database, then read the data back to the user.  Will refactor later.
    """

    @abstractmethod
    def check_connection(self):
        pass

    @abstractmethod
    def initialize_registry(self):
        pass

    @abstractmethod
    def close_registry_connection(self):
        pass

    @abstractmethod
    def get_user_list(self):
        pass

    @abstractmethod
    def get_content_list(self):
        pass

    @abstractmethod
    def registry_description(self) -> dict:
        pass


class SQLiteRegistry(ContentRegistry):
    def __init__(self):
        self.connection: sqlite3.Error = None
        self.migrations_ran: bool = False

    def check_connection(self):
        if not self.connection:
            raise RegistryNotInitializedException(
                "No SQLite connection initialized!  Run initialize_registry."
            )

        if not self.migrations_ran:
            raise RegistryNotInitializedException(
                "ContentRegistry setup incomplete; view README for installation instructions."
            )

    def initialize_registry(self):
        # we want to bubble the error up to print it for now
        self.connection = sqlite3.connect(":memory:")
        cursor = self.connection.cursor()
        table_list = cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type IN ('table','view')
            AND name NOT LIKE 'sqlite_%'
            ORDER BY 1;
            """
        ).fetchall()

        if len(table_list) > 0:
            self.migrations_ran = True

    def get_user_list(self):
        pass

    def get_content_list(self):
        pass

    def registry_description(self) -> dict:
        pass

    def close_registry_connection(self):
        pass
