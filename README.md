# Fake Data To Database

**Fake Data To Database** is a Python library designed to generate fake data and insert it into databases.

## Features
- Generate realistic fake data using `Faker`
- Insert data into:
  - PostgreSQL
  - SQLServer
- Easy-to-use interface for bulk data insertion

## Installation

You can install the library using pip:

```bash
pip install fake-data-to-database
```

## Exemple of use
You can use the lib as the exemple:

```python
import fake_data_to_database as fdg

db_config_postgres = {
    "db": "postgres",
    "host": "localhost",
    # "port": 5432, # Default 5432
    "database": "testdb",
    "user": "user",
    "password": "password",
}
db_config_sqlserver = {
    "db": "sqlserver",
    "host": "localhost",
    # "port": 1433, # Default 1433
    "database": "master",
    "user": "SA",
    "password": "YourStrong!Passw0rd",
}

fields = {
    "name": {"type": "varchar", "nullable": False},
    "age": {"type": "int", "nullable": False},
    "email": {"type": "varchar", "nullable": True},
    "cidade": {"type": "varchar", "nullable": False},
}

fdg = fdg.FakeDataGenerator(
    db_config=db_config_sqlserver,
    schema="test",
    table="test",
    fields_config=fields
)

fdg.generate_and_insert_data(num_records=10)

```