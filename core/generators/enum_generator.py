from .base_generator import BaseFieldGenerator
import random



class EnumValueGenerator(BaseFieldGenerator):
    """
    Chooses a random value from a predefined list, with optional weights.

    Config format:
    values: [a, b, c]
    weights: [0.5, 0.3, 0.2]
    """
    
    def generate(self, row_idx, row_data):
        values = self.config['values']
        weights = self.config.get('weights')
        return random.choices(values, weights=weights, k=1)[0]