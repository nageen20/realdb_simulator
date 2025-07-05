from pathlib import Path
import pandas as pd
import sys
import logging

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)

from utils.faker_instance import get_faker

# Import all generators
from core.generators.base_generator import BaseFieldGenerator
from core.generators.location_generator import FakerLocationGenerator
from core.generators.fetch_from_file_generator import FetchFromFileGenerator
from core.generators.dependent_field_generator import DependentFieldGenerator
from core.generators.enum_generator import EnumValueGenerator
from core.generators.review_text_generator import ReviewTextGenerator
from core.generators.simple_faker_generator import SimpleFakerFieldGenerator
from core.generators.primary_key_generator import PrimaryKeyGenerator
from core.generators.foreign_key_generator import ForeignKeyGenerator

faker = get_faker()

logger = logging.getLogger(__name__)

class TableDataGenerator:
    def __init__(self, table_name, table_config, global_data_dir, fk_lookup=None):
        self.table_name = table_name
        self.columns = table_config['columns']
        self.num_rows = table_config.get('rows', 100)
        self.global_data_dir = Path(global_data_dir)
        self.distribution = table_config.get('distribution', 'uniform')
        self.primary_keys = table_config.get('primary_keys') or table_config.get('primary_key', [])
        self.foreign_keys = table_config.get('foreign_keys', {})
        self.fk_lookup = fk_lookup or {}
        self.field_generators = self._initialize_field_generators()

    def _initialize_field_generators(self):
        generators = {}
        lookup_cache = {}

        for field_name, config in self.columns.items():
            if field_name in self.primary_keys:
                generators[field_name] = PrimaryKeyGenerator(field_name)

            elif field_name in self.foreign_keys:
                logger.info(f'Reference table is: {self.foreign_keys[field_name]}')
                ref_table = self.foreign_keys[field_name].split('.')[0]
                ref_column = self.foreign_keys[field_name].split('.')[1]
                reference_values = self.fk_lookup.get(ref_table, {}).get(ref_column, [])
                generators[field_name] = ForeignKeyGenerator(field_name, reference_values)

            elif 'values' in config:
                generators[field_name] = EnumValueGenerator(field_name, config)

            elif config.get('type') == 'review_text':
                generators[field_name] = ReviewTextGenerator(field_name, config)

            elif config.get('group') == 'location':
                generators[field_name] = FakerLocationGenerator(field_name, config)

            elif 'source_file' in config:
                source_file = config['source_file']
                if source_file not in lookup_cache:
                    csv_path = self.global_data_dir / source_file
                    lookup_cache[source_file] = pd.read_csv(csv_path)
                df = lookup_cache[source_file]

                if config.get('depends_on'):
                    generators[field_name] = DependentFieldGenerator(field_name, config, df)
                else:
                    generators[field_name] = FetchFromFileGenerator(field_name, config, df)

            elif config.get('type') in dir(get_faker()):
                generators[field_name] = SimpleFakerFieldGenerator(field_name, config, self.fk_lookup)

        return generators
    

    def generate_rows(self):
        rows = []
        for i in range(self.num_rows):
            row = {}
            for field_name, generator in self.field_generators.items():
                try:
                    value = generator.generate(i, row)
                    if isinstance(value, dict):
                        row.update(value)
                    else:
                        row[field_name] = value
                except Exception as e:
                    logging.error(f"Error in table={self.table_name}, field={field_name}, row={i}")
                    raise e
            rows.append(row)
        return rows
    

    def generate_and_update_fk_lookup(self):
        rows = self.generate_rows()
        df = pd.DataFrame(rows)

        # Initialize nested dict for this table
        self.fk_lookup[self.table_name] = {}

        for col in df.columns:
            if col in self.primary_keys:
                # For dependent lookups (like order_date depending on signup_date), use ID → value mapping
                self.fk_lookup[self.table_name][col] = df[col].tolist()
            else:
                logger.info(self.primary_keys)
                self.fk_lookup[self.table_name][col] = {
                    pk: val for pk, val in zip(df[self.primary_keys[0]], df[col])
                }

        return df
