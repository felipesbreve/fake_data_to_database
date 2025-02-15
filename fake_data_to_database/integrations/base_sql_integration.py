import abc


class BaseSQLIntegration(abc.ABC):
    def __init__(self):
        self.conn = None
        self.cursor = None

    def execute_query(self, query: str):
        """Executes a given SQL query."""
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise f"Error executing query: {e}"

    @abc.abstractmethod
    def connect(self):
        """Abstract method to establish a database connection."""
        pass

    def insert_data(self, db_config: str, table: str, fields: list, values: list):
        """Inserts data into the specified SQL table."""

        placeholders = ', '.join(['?' if db_config == "sqlserver" else '%s'] * len(fields))
        query = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders});"
        self.cursor.execute(query, values)

    def insert_batch(self, db_config: str, schema: str, table: str, fields: list, values_list: list):
        """Inser multiples rows at once into the specified SQL table."""

        placeholders = ', '.join(['?' if db_config == "sqlserver" else '%s'] * len(fields))        
        fields_str = ', '.join(fields)
        query = f'INSERT INTO {schema}.{table} ({fields_str}) VALUES ({placeholders})'

        try:
            self.cursor.executemany(query, values_list)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error insertind data: {e}")

    def commit(self):
        """Commits the transaction."""
        if self.conn:
            self.conn.commit()

    def close(self):
        """Closes the database connection."""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
