import random
from faker import Faker
from pathlib import Path
import pandas as pd
from datetime import datetime, timedelta

faker = Faker()


class BaseFieldGenerator:
    def __init__(self, field_name, config):
        self.field_name = field_name
        self.config = config

    def generate(self, row_idx, row_data):
        raise NotImplementedError