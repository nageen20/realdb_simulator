from faker import Faker

_faker_instance = Faker()

def get_faker():
    return _faker_instance
