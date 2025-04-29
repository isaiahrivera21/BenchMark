# should populate the food database to have intial values. 

from django.core.management.base import BaseCommand, CommandError
from foodrepo.models import FoodEntry
from dotenv import load_dotenv
import os
import requests
from pprint import pprint
from django.db import transaction


NUTRIENT_MAPPING = {
    'Energy': 'calories',
    'Total lipid (fat)': 'fat',
    'Carbohydrate, by difference': 'carbohydrates',
    'Protein': 'protein',
    'Cholesterol': 'cholesterol',
    'Sodium, Na': 'sodium',
    'Total Sugars': 'sugars',
}

class Command(BaseCommand):
    help = "Populates food database"


    def handle(self,*args,**kwargs):
        all_foods = []
        self.stdout.write("Starting to pull data from food api")
        
        load_dotenv()
        api_key = os.getenv("USDA_API_KEY")
        # demo_key = 'DEMO_KEY'
        api_url =  f'https://api.nal.usda.gov/fdc/v1/foods/list?api_key={api_key}'
        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                # Convert response to JSON
                data = response.json() 


               

                self.stdout.write(f"Successfully retrieved {len(data)} items from the API.")

                # for item in data:
                #     self.stdout.write(f"ID: {item.get('fdcId')} | Name: {item.get('description')}")

                # for item in data:
                #     pprint(data)
                #     print("\n")

            else:
                self.stderr.write(f"Failed to fetch data: {response.status_code} - {response.text}")

            
            def extract_nutrients(food):
                nutrients = {}
                for nutrient in food.get('foodNutrients', []):
                    name = nutrient.get('name')
                    value = nutrient.get('amount')
                    if name in NUTRIENT_MAPPING and value is not None:
                        nutrients[NUTRIENT_MAPPING[name]] = value
                return nutrients
            
            food_instances = []
            for food in data:
                item = extract_nutrients(food)
                # Check if required fields have valid values
                if item.get('calories') is not None:
                    instance = FoodEntry(
                        food_name=food.get('description', ''),
                        calories=item.get('calories'),
                        fat=item.get('fat'),
                        carbohydrates=item.get('carbohydrates'),
                        protein=item.get('protein'),
                        cholesterol=item.get('cholesterol'),
                        sodium=item.get('sodium'),
                        sugars=item.get('sugars'),
                    )
                    food_instances.append(instance)

            

            FoodEntry.objects.bulk_create(food_instances)

            self.stdout.write(self.style.SUCCESS("Successfully populated food database"))

        
        except requests.exceptions.RequestException as e:
            # should send stuff to std err 
            self.stderr.write(e)

    # food1.get('description')
    # (food1.get('foodNutrients')[0].get('name')) # can get the nutirents name but once again sad for loop parsing 


