from .base_generator import BaseFieldGenerator
import random

class ReviewTextGenerator(BaseFieldGenerator):
    """
    Generates a realistic review text based on the rating value of a product or service.

    This generator selects a review template based on the sentiment implied by the `rating` column:
    - If rating is 4 or 5 → chooses from positive reviews.
    - If rating is 3 → chooses from neutral reviews.
    - If rating is 1 or 2 → chooses from negative reviews.
    - If no rating is present, defaults to a random rating between 1 and 5.

    This is useful for simulating user-generated review content for e-commerce, service platforms, etc.

    Attributes:
        POSITIVE_TEMPLATES (List[str]): Sample reviews for positive sentiment.
        NEGATIVE_TEMPLATES (List[str]): Sample reviews for negative sentiment.
        NEUTRAL_TEMPLATES (List[str]): Sample reviews for neutral sentiment.

    Example Usage:
        If row_data = {'rating': 5}, this generator will return a randomly chosen positive review string.
    """
    
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
