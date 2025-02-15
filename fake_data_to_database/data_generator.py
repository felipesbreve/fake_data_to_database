import random
from faker import Faker
from typing import Optional, Any


class DataGenerator:
    FIELD_MAPPINGS = {
        "name": ["name", "nome", "full_name"],
        "first_name": ["primeiro_nome", "first_name"],
        "last_name": ["sobrenome", "last_name"],
        "city": ["city", "cidade"],
        "email": ["email", "e-mail"],
        "phone": ["phone", "telefone", "celular", "mobile"],
        "address": ["address", "endereco", "rua", "logradouro"],
        "state": ["state", "estado", "province"],
        "country": ["country", "pais"],
        "company": ["company", "empresa"],
        "job": ["job", "profissao", "cargo"],
        "product": ["product", "produto"],
        "category": ["category", "categoria"],
        "age": ["age", "idade"],
        "value": ["value", "valor", "price", "preço"]
    }

    def __init__(self, locale=["pt_BR"]):
        """
        Initializes the DataGenerator with the provided locale(s).
        :param locale: A list of locales (e.g., ["pt_BR", "en_US"]) for the Faker instance.
        """
        self.fake = Faker(locale)

    def detect_field_type(self, column_name: str) -> str:
        """
        Detects the expected data type based on the column name.
        Returns a string corresponding to the detected field type.
        
        :param column_name: The name of the column to detect the type for.
        :return: A string representing the detected field type (e.g., 'name', 'int', 'varchar').
        """
        column_name = column_name.lower().strip()  # Normalize the column name

        # Iterate over the synonyms for each field type to find a match
        for field_type, synonyms in self.FIELD_MAPPINGS.items():
            if column_name in synonyms:
                return field_type

        return "text"  # Default to 'text' if no match is found

    def get_generator(self, field_type: str, column_name: str):
        """
        Returns the generator function associated with the provided or detected field type.
        If the field type is mapped, it uses the mapped generator; if not, it uses the provided type.
        
        :param field_type: The type of the field (e.g., 'int', 'varchar').
        :param column_name: The name of the column to check if it has a mapped type.
        :return: A function that generates the appropriate data based on the field type.
        """
        # Check if the column name has a mapped field type
        field_type_mapped = self.detect_field_type(column_name)

        # If the field has a mapped type, return the corresponding generator
        if field_type_mapped != "text":
            generators = {
                "name": self.fake.name,
                "first_name": self.fake.first_name,
                "last_name": self.fake.last_name,
                "city": self.fake.city,
                "email": self.fake.email,
                "phone": self.fake.phone_number,
                "address": self.fake.address,
                "state": self.fake.state,
                "country": self.fake.country,
                "company": self.fake.company,
                "job": self.fake.job,
                "product": self.fake.word,
                "category": self.fake.word,
                "age": lambda: random.randint(18, 80),  # Age generator for 'int'
                "value": lambda: round(random.uniform(1.0, 10000.0), 2),  # Value generator for 'float'
            }
            return generators.get(field_type_mapped, self.fake.word)

        # If the field type is not mapped, use the provided field type and return the corresponding generator
        if field_type == "int" or field_type_mapped == "int":
            return lambda: random.randint(1, 1000)
        elif field_type == "float" or field_type_mapped == "float":
            return lambda: round(random.uniform(1.0, 1000.0), 2)
        elif field_type == "varchar" or field_type_mapped == "varchar":
            return self.fake.word
        elif field_type == "text" or field_type_mapped == "text":
            return lambda: self.fake.text(max_nb_chars=200)
        elif field_type == "boolean" or field_type_mapped == "boolean":
            return lambda: random.choice([True, False])
        else:
            raise ValueError(f"Field type '{field_type}' is not mapped.")

    def generate_data(self, column_name: str, field_type: str, nullable: bool = False) -> Optional[Any]:
        """
        Generates fake data based on the provided field type.
        If `allow_null` is True, there is a 10% chance of returning None.
        
        :param column_name: The name of the column to generate data for.
        :param field_type: The type of the field (e.g., 'int', 'varchar', etc.).
        :return: A value generated based on the field type (e.g., a string, integer, or boolean).
        """
        # Get the generator corresponding to the field type
        generator = self.get_generator(field_type, column_name)

        # Generate and return the data
        return generator()
