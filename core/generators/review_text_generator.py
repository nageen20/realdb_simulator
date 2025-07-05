from .base_generator import BaseFieldGenerator
import random

class ReviewTextGenerator(BaseFieldGenerator):
    POSITIVE_TEMPLATES = [
        "Absolutely loved this product! It exceeded my expectations.",
        "Works great, very satisfied with the quality.",
        "Fast delivery and excellent customer support.",
        "Highly recommend this to anyone looking for quality."
    ]

    NEGATIVE_TEMPLATES = [
        "Terrible experience. Would not recommend.",
        "The product did not match the description.",
        "Shipping was delayed and support was unhelpful.",
        "Really disappointed with this purchase."
    ]

    NEUTRAL_TEMPLATES = [
        "It's okay, does the job but nothing exceptional.",
        "Average quality for the price.",
        "Neither good nor bad – just what I expected.",
        "Service was fine, product is decent."
    ]

    def generate(self, row_idx, row_data):
        sentiment = row_data.get("rating", random.randint(1, 5))
        if sentiment >= 4:
            return random.choice(self.POSITIVE_TEMPLATES)
        elif sentiment == 3:
            return random.choice(self.NEUTRAL_TEMPLATES)
        else:
            return random.choice(self.NEGATIVE_TEMPLATES)
