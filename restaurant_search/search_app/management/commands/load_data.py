import csv
import json  # Import json module
from django.core.management.base import BaseCommand
from search_app.models import Dish

class Command(BaseCommand):
    help = 'Load restaurant data from CSV'

    def handle(self, *args, **kwargs):
        with open('search_app/management/data/restaurants_small.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    items_with_prices = json.loads(row['items'])
                except json.JSONDecodeError:
                    items_with_prices = {}
                
                items = ', '.join([f"{item} - {price}" for item, price in items_with_prices.items()])  # Convert items with prices to string
                
                try:
                    full_details = json.loads(row['full_details'])
                    rating = float(full_details['user_rating']['aggregate_rating'])
                except (json.JSONDecodeError, KeyError, ValueError):
                    rating = 0.0  # Default rating if parsing fails
                
                Dish.objects.create(
                    name=row['name'],
                    restaurant_name=row['name'],
                    location=row['location'],
                    items=items,
                    prices=json.dumps(items_with_prices),  # Store the raw JSON data in the prices field
                    rating=rating
                )
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
