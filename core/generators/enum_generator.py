from .base_generator import BaseFieldGenerator
import random



class EnumValueGenerator(BaseFieldGenerator):
    def generate(self, row_idx, row_data):
        values = self.config['values']
        weights = self.config.get('weights')
        return random.choices(values, weights=weights, k=1)[0]