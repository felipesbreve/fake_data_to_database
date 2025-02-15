# Fake Data Generator

**Fake Data Generator** is a Python library designed to generate fake data and insert it into various databases, including MySQL, SQL Server, PostgreSQL, MongoDB and BigQuery.

## Features
- Generate realistic fake data using `Faker`
- Insert data into:
  - PostgreSQL
- Easy-to-use interface for bulk data insertion

## Installation

You can install the library using pip:

<!-- ```bash
pip install fake-data-generator
``` -->

Exemple of use
```python
import fake_data_generator as fdg

db_config_postgres = {
    "db": "postgres",
    "host": "localhost",
    "port": 5432,
    "database": "db",
    "user": "user",
    "password": "password",
}

fields = {
    "name": {"type": "varchar", "nullable": False},
    "age": {"type": "int", "nullable": False},
    "email": {"type": "varchar", "nullable": True},
    "cidade": {"type": "varchar", "nullable": False},
}

fdg = fdg.FakeDataGenerator(
    db_config=db_config_postgres,
    schema="public",
    table="teste",
    fields_config=fields
)

fdg.generate_and_insert_data(num_records=10)

```