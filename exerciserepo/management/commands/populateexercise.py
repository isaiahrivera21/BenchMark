# should populate the food database to have intial values. 

from django.core.management.base import BaseCommand, CommandError
from exerciserepo.models import Exercise
from dotenv import load_dotenv
import os
import requests
from pprint import pprint



class Command(BaseCommand):
    help = "Populates exercise database"

    


    def handle(self,*args,**kwargs):
        self.stdout.write("Starting to pull data from exercise api")
        all_exercises = []
        PAGE = 0
        
        # load_dotenv()
        # api_key = os.getenv("USDA_API_KEY")
        # # demo_key = 'DEMO_KEY'

        api_url = "https://exercisedb-api.vercel.app/api/v1/exercises"
        offset = 0
        limit = 100  # Adjust as needed
        try:
            while True:

                if PAGE == 2: break


                params = {"offset": offset, "limit": limit}
                response = requests.get(api_url, params=params)
                
                if response.status_code != 200:
                    print("Error:", response.status_code)
                    break

                data = response.json()['data']
                exercises = data['exercises']
                all_exercises.extend(exercises)

                if not data['nextPage']:  # Stop if there's no next page
                    break

                offset += limit  # Move to the next set of exercises

                PAGE += 1
        
            breakpoint() # <-- sp this get us what we want. Now we have to find a way to bulk insert it into the database


        
        except requests.exceptions.RequestException as e:
            # should send stuff to std err 
            self.stderr.write(e)
