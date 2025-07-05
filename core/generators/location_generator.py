from .base_generator import BaseFieldGenerator
from pathlib import Path
import sys

path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)

from utils.faker_instance import get_faker

class FakerLocationGenerator(BaseFieldGenerator):

    """
    Generates a location dictionary with related values for city, state, and country 
    using faker.location_on_land(). Useful for address or geolocation data.
    """

    def generate(self, row_idx, row_data):
        faker = get_faker()
        _, _, city, country, state = faker.location_on_land()
        return {
            'city': city,
            'state': state,
            'country': country,
        }
