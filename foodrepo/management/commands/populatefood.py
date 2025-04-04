# should populate the food database to have intial values. 

from django.core.management.base import BaseCommand, CommandError
from foodrepo.models import FoodEntry
from dotenv import load_dotenv
import os
import requests
from pprint import pprint



class Command(BaseCommand):
    help = "Populates food database"


    def handle(self,*args,**kwargs):
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

                for item in data:
                    self.stdout.write(f"ID: {item.get('fdcId')} | Name: {item.get('description')}")

                # for item in data:
                #     pprint(data)
                #     print("\n")


            else:
                self.stderr.write(f"Failed to fetch data: {response.status_code} - {response.text}")

        
        except requests.exceptions.RequestException as e:
            # should send stuff to std err 
            self.stderr.write(e)

    