from .base_generator import BaseFieldGenerator
import random

class ForeignKeyGenerator(BaseFieldGenerator):
    """
    Picks a random foreign key value from the referenced table's values.

    Args:
        reference_values (List[Any]): Valid foreign key values.
    """
    
    def __init__(self, field_name, reference_values):
        super().__init__(field_name, {})
        self.reference_values = reference_values

    def generate(self, row_idx, row_data):
        return random.choice(self.reference_values)
