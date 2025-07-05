from .base_generator import BaseFieldGenerator

class PrimaryKeyGenerator(BaseFieldGenerator):
    def __init__(self, field_name):
        super().__init__(field_name, {})

    def generate(self, row_idx, row_data):
        return row_idx + 1 