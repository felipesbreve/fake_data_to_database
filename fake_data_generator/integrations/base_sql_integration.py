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
            print(f"Error executing query: {e}")

    @abc.abstractmethod
    def connect(self):
        """Abstract method to establish a database connection."""
        pass

    def insert_data(self, table: str, fields: list, values: list):
        """Inserts data into the specified SQL table."""
        placeholders = ", ".join(["%s"] * len(values))
        query = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders});"
        self.cursor.execute(query, values)

    def insert_batch(self, schema: str, table: str, fields: list, values_list: list):
        """Inser multiples rows at once into the PostgreSQL database."""
        placeholders = ', '.join(['%s'] * len(fields))
        fields_str = ', '.join(fields)
        query = f'INSERT INTO {schema}.{table} ({fields_str}) VALUES ({placeholders})'

        try:
            self.cursor.executemany(query, values_list)  # Insere todas as linhas de uma vez
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()  # Desfaz a transação em caso de erro
            print(f"Erro ao inserir dados: {e}")

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
