import psycopg2
from .base_sql_integration import BaseSQLIntegration


class PostgreSQLIntegration(BaseSQLIntegration):
    def __init__(self, database: str, user: str, password: str, host: str = 'localhost', port: int = 1433, server: str = None):
        super().__init__()
        self.host = server if host == None else host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connect()

    def connect(self):
        """Establishes a connection to the PostgreSQL database."""
        self.conn = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        self.cursor = self.conn.cursor()

    def __enter__(self):
        """Allows using 'with' statements for automatic resource management."""
        if self.conn is None:
            self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Closes the connection when exiting the 'with' block."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
