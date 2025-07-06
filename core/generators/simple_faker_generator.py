from .base_generator import BaseFieldGenerator
from pathlib import Path
import sys
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)

from utils.faker_instance import get_faker

class SimpleFakerFieldGenerator(BaseFieldGenerator):
    """
    A generator that uses the Faker library to produce synthetic data for standard fields like
    phone numbers, emails, integers, floats, and dates.

    It supports:
    - Simple faker types like `email`, `uuid4`, `phone_number`, `name`. `company`, `city`.
    - Range-based values for numeric and datetime types.
    - Boundaries (`min`, `max`, `start_date`, `end_date`) that can:
        • be static values
        • be relative (e.g., "+30d", "-365d")
        • depend on other tables via foreign key references like "orders.order_date"

    Parameters:
        field_name (str): The name of the field/column.
        config (dict): The schema config for the field.
        fk_lookup (dict): A nested dictionary of reference values for foreign key resolution.

    Methods:
        - generate(row_idx, row_data): Generates a value for a given row based on config and FK context.

    Example YAML usage:
    ```yaml
    signup_date:
      type: date_between
      data_type: DATE
      start_date: "-365d"
      end_date: "now"

    order_date:
      type: date_time_between
      data_type: datetime
      start_date: customers.signup_date
      end_date: "now"
    ```

    Notes:
        - Dates are interpreted via `_resolve_bound`, which can handle:
            * relative offsets (`+10d`, `-7d`)
            * foreign references like `orders.order_date`
        - It logs errors when invalid ranges or null dependencies are encountered.
    """

    def __init__(self, field_name, config, fk_lookup):
        super().__init__(field_name, config)
        self.fk_lookup = fk_lookup

    
    def _resolve_bound(self, bound, row_data):
        if isinstance(bound, (int, float)):
            return bound
        if isinstance(bound, str):
            if bound == 'now':
                return bound
            if bound.endswith('d'):
                try:
                   return bound
                except ValueError:
                    return datetime.now()
            if '.' in bound:
                table, column = bound.split('.')
                fk_field = f"{table}_id"
                fk_value = row_data.get(fk_field)
                table_data = self.fk_lookup.get(table, {}).get(column)
                if isinstance(table_data, dict):
                    return table_data.get(fk_value)
                elif isinstance(table_data, list):
                    for row in table_data:
                        if row.get('id') == fk_value:
                            return row.get(column)
        return 'now'


    def generate(self, row_idx, row_data):
        faker = get_faker()
        faker_fn = getattr(faker, self.config['type'])
        try:
            if self.config['type'] in ['random_int', 'pyint']:
                min_val = self.config.get('min', 0)
                max_val = self.config.get('max', min_val+100)
                return faker_fn(min=min_val, max=max_val)

            elif self.config['type'] in ['pydecimal', 'pyfloat']:
                min_val = self._resolve_bound(self.config.get('min', 0), row_data)
                max_val = self._resolve_bound(self.config.get('max', min_val+100), row_data)
                return faker_fn(right_digits=2, min_value=min_val, max_value=max_val)

            elif self.config['type'] in ['date_between', 'date_time_between']:
                start_date = self._resolve_bound(self.config.get('start_date', '-30d'), row_data)
                end_date = self._resolve_bound(self.config.get('end_date', 'now'), row_data)

                if start_date is None or end_date is None:
                        logger.error(
                            f"[{self.field_name}] Invalid date range: start={start_date}, end={end_date}, row={row_data}"
                        )
                        raise ValueError(f"Invalid date range: {start_date} to {end_date}")


                return faker_fn(start_date=start_date, end_date=end_date)
            
            elif self.config['type'] in ['phone_number','email','name','uuid4','company','city']:
                return faker_fn()

            return faker_fn()
        
        except Exception as e:
            logger.exception(f"[{self.field_name}] Error generating value for row {row_idx} with config: {self.config}")
            raise e