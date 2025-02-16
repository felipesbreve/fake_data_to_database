# Fake Data To Database

A Python library for generating and inserting fake data into SQL Server and PostgreSQL databases.

## Table of Contents
- [Description](#description)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)

## Description
The library currently supports:

* PostgreSQL
* SQL Server

Fake Data To Database simplifies the generation of fake data and its direct insertion into databases, ideal for testing, development, and simulations.



## Installation

Before starting, make sure you have Python installed.

```sh
pip install fake-data-to-database
```

## Configuration

Configure the database credentials in the `db_config` dictionarie.

Example:
```python
db_config = {
    "db": "db",
    "database": "your_database",
    "user": "your_user",
    "password": "your_password",
}
```
### Parameters

- **`db`** (`str`) **(required)**: Specifies the type of database. Accepted values:
  - `postgres`: For PostgreSQL database.
  - `sqlserver`: For SQL Server database.

- **`database`** (`str`) **(required)**: The name of the database you want to connect to.

- **`user`** (`str`) **(required)**: The username used for authentication to the database.

- **`password`** (`str`) **(required)**: The password for the provided username for authentication.

- **`host`** (`str`) **(optional, default: `localhost`)**: The address of the database server (can also be referred to as `server`).

- **`port`** (`int`) **(optional, default:)**: The port number for the database connection. Default values:
  - **5432** for PostgreSQL.
  - **1433** for SQL Server.

## Usage
Basic example of generation and insertion:

```python
import fake_data_to_database as fdg

fields = {
    "name": {"type": "varchar"},
    "age": {"type": "int"},
    "email": {"type": "varchar", "nullable": True},
    "city": {"type": "varchar"},
}

fdg = fdg.FakeDataGenerator(
    db_config=db_config,
    schema="your_schema",
    table="your_table",
    fields_config=fields
)

fdg.generate_and_insert_data(num_records=10)

```

### `fdg.FakeDataGenerator`

This class is used to generate fake data for testing purposes. It connects to a specified database and generates data based on a provided schema, table, and fields configuration.

#### Parameters

- **`db_config`** (`dict`) **(required)**: The database configuration dictionary

- **`schema`** (`str`) **(required)**: The schema within the database where the table resides. It can also be referred to as `dataset`.

- **`table`** (`str`) **(required)**: The name of the table where the fake data will be inserted or used.

- **`fields_config`** (`dict`) **(required)**: A dictionary that specifies the configuration of the fields to be generated. Each key should have the keys:
    - **`type`** (`str`) **(required)**: Type of the field, that can be:
        - int
        - float
        - varchar
        - text
        - boolean
    - **`nullable`** (`bool`) **(optional, default: `False`)**: Specifies if the field is nullable.

- **`has_id`** (`bool`) **(optional, default: `True`)**: Indicates whether the generated records should include an `id` field. If `True`, an `id` will be included as the primary key for each record.

### `fdg.generate_and_insert_data`
This method generates fake data based on the provided `fields_config` and inserts it into the specified database table.

#### Parameters
- **`num_records`** (`int`) **(required)**: The number of fake records to generate and insert into the database.

- **`NULLABLE_SEED`** (`float`) **(optional, default: `0.1`)**: The probability (between 0 and 1) that a field marked as `nullable` will have a `NULL` value. This determines how many nullable fields will be populated with `NULL` values.

- **`batch_size`** (`int`) **(optional, default: `100`)**: The number of records to insert into the database in each batch. This helps optimize the insertion process by splitting the data into smaller chunks rather than inserting all records at once.