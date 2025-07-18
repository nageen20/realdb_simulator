from faker import Faker
import random
import datetime

faker = Faker()

def generate_fake_value(field_type: str):
    if isinstance(field_type, dict):
        field_type = field_type.get("type", "string")
    if not isinstance(field_type, str):
        raise ValueError(f"Unexpected field_type: {field_type}")
   # else:        
   #     field_type = field_type.lower().strip()

    # Strip pk/fk suffix
    if 'pk' in field_type:
        return None  # Will be auto-generated by index or handled separately
    if 'fk:' in field_type:
        return None  # Handled via foreign key assignment

    if "int" in field_type:
        return random.randint(1, 1000)
    elif "float" in field_type:
        return round(random.uniform(1.0, 100.0), 2)
    elif "name" in field_type:
        return faker.name()
    elif "company" in field_type:
        return faker.company()
    elif "city" in field_type:
        return faker.city()
    elif "word" in field_type:
        return faker.word()
    elif "phone" in field_type:
        return faker.phone_number()
    elif "email" in field_type:
        return faker.email()
    elif "datetime" in field_type:
        return faker.date_time_between(start_date="-1y", end_date="now")
    elif "date" in field_type:
        return faker.date_between(start_date="-1y", end_date="today")
    elif "bool" in field_type:
        return random.choice([True, False])
    elif "text" in field_type:
        return faker.text(max_nb_chars=50)
    else:
        return faker.word()
