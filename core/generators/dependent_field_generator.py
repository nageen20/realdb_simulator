from .base_generator import BaseFieldGenerator
import random
import pandas as pd

class DependentFieldGenerator(BaseFieldGenerator):
    def __init__(self, field_name, config, lookup_df):
        super().__init__(field_name, config)
        self.lookup_df = lookup_df
        self.source_column = field_name#config['column']
        self.depends_on = config.get('depends_on')
        self.formula_type = config.get('dependent_formula', 'hierarchy')
        self.conditions = config.get('conditions', {})

    def generate(self, row_idx, row_data):
        parent_value = row_data.get(self.depends_on)

        if self.formula_type == 'equals':
            return parent_value

        elif self.formula_type == 'pandas':
            formula = self.config.get('formula')
            if formula:
                try:
                    context = {'df': self.lookup_df, 'row_data': row_data, 'pd': pd}
                    return eval(formula, context)
                except Exception as e:
                    print(f"Error evaluating formula for {self.field_name}: {e}")
                    return None
        
        elif self.formula_type == 'conditional':
            possible_values = self.conditions.get(parent_value, [])
            if possible_values:
                return random.choice(possible_values)
            return None

        # Default hierarchy logic
        subset = self.lookup_df[self.lookup_df[self.depends_on] == parent_value]
        if subset.empty:
            return random.choice(self.lookup_df[self.source_column].tolist())
        return random.choice(subset[self.source_column].tolist())