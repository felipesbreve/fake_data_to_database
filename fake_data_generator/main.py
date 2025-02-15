from .data_generator import DataGenerator
from .integrations import (
    PostgreSQLIntegration
)
from typing import Dict, Any


class FakeDataGenerator:
    def __init__(self, db_config: Dict[str, Any], schema: str, table: str, fields_config: Dict[str, Dict[str, Any]]):
        self.data_gen = DataGenerator()
        self.db_config = db_config
        self.schema = schema
        self.table = table
        self.fields_config = fields_config
        self.db_integration = self._get_db_integration(db_config["db"])

    def _get_db_integration(self, db_type: str) -> Any:
        """Returns the correct database integration class based on the database type."""
        integrations = {
            "postgres": PostgreSQLIntegration,
        }

        if db_type not in integrations:
            raise ValueError(f"Unsupported database type: {db_type}")
        
        db_params = {k: v for k, v in self.db_config.items() if k != "db"}

        return integrations[db_type](**db_params)
    
    def _create_table_if_not_exists(self, db):
        """Checks if the table exists and creates it if necessary."""
        create_statements = {
            "postgres": f"""
                CREATE TABLE IF NOT EXISTS {self.schema}.{self.table} (
                    {', '.join([f'{col} {self._map_type(config["type"])} {"NULL" if config.get("nullable", False) else "NOT NULL"}'
                                for col, config in self.fields_config.items()])}
                );
            """
        }

        db.execute_query(create_statements[self.db_config["db"]])

    @staticmethod
    def _map_type(field_type: str) -> str:
        """Maps generic field types to SQL-specific data types."""
        type_mapping = {
            "int": "INTEGER",
            "float": "FLOAT",
            "varchar": "VARCHAR(255)",
            "text": "TEXT",
            "date": "DATE",
            "datetime": "TIMESTAMP",
            "boolean": "BOOLEAN"
        }
        return type_mapping.get(field_type, "TEXT")  # Default to TEXT if type unknown

    def generate_and_insert_data(self, num_records: int):
        """Generates fake data and inserts it into the database."""
        fields = list(self.fields_config.keys())
        
        with self.db_integration as db:
            self._create_table_if_not_exists(db)

            batch_size = 100
            batch = []

            for _ in range(num_records):
                values = [
                    self.data_gen.generate_data(column_name, config["type"])
                    for column_name, config in self.fields_config.items()
                ]
                batch.append(values)

                if len(batch) >= batch_size:
                    db.insert_batch(self.schema, self.table, fields, batch)
                    batch.clear()

            if batch:
                db.insert_batch(self.schema, self.table, fields, batch)

        print(f"{num_records} records inserted into {self.schema}.{self.table}.")