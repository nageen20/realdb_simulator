from .base_generator import BaseFieldGenerator
import random


class FetchFromFileGenerator(BaseFieldGenerator):
    """
    Fetches values randomly from a specified column in an external CSV file.
    
    Args:
        field_name (str): Column to generate.
        config (dict): YAML field config.
        lookup_df (pd.DataFrame): DataFrame loaded from source_file.
    """
    
    def __init__(self, field_name, config, lookup_df):
        super().__init__(field_name, config)
        self.lookup_df = lookup_df
        self.source_column = field_name#config['column']

    def generate(self, row_idx, row_data):
        return random.choice(self.lookup_df[self.source_column].tolist())