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
    def check_connection():
        pass

    @abstractmethod
    def initialize_registry():
        pass

    @abstractmethod
    def close_registry_connection():
        pass

    @abstractmethod
    def get_user_list():
        pass

    @abstractmethod
    def get_content_list():
        pass

    @abstractmethod
    def registry_description() -> dict:
        pass

class SQLiteRegistry(ContentRegistry):
    def __init__(self):
        self.connection: sqlite3.Error = None

    def check_connection(self):
        if not self.connection:
            raise RegistryNotInitializedException("No SQLite connection initialized!")

    def initialize_registry(self):
        # we want to bubble the error up to print it for now
        self.connection = sqlite3.connect(":memory:")
        cursor = self.connection.cursor()
        cursor.execute()

    def get_user_list(self):
        pass

    def get_content_list(self):
        pass

    def registry_description(self) -> dict:
        pass

    def close_registry_connection():
        pass


