# should populate the food database to have intial values.

from django.core.management.base import BaseCommand, CommandError
from exerciserepo.models import ExerciseEntry
from dotenv import load_dotenv
import os
import requests
from pprint import pprint
from django.db import transaction


class Command(BaseCommand):
    help = "Populates exercise database"

    def handle(self, *args, **kwargs):
        PAGE = 0
        self.stdout.write("Starting to pull data from exercise api")
        all_exercises = []
        api_url = "https://exercisedb-api.vercel.app/api/v1/exercises"
        offset = 0
        limit = 100
        try:
            while True:

                if PAGE == 2:  # only limited to two pages
                    break

                params = {"offset": offset, "limit": limit}
                response = requests.get(api_url, params=params)

                if response.status_code != 200:
                    print("Error:", response.status_code)
                    break

                data = response.json()["data"]
                exercises = data.get("exercises", [])
                all_exercises.extend(exercises)

                if not data["nextPage"]:  # Stop if there's no next page
                    break

                offset += limit  # Move to the next set of exercises

                PAGE += 1

            exercise_instances = [
                ExerciseEntry(
                    exercise_name=item.get("name", ""),
                    target_muscles=item.get("targetMuscles", ""),
                )
                for item in all_exercises
            ]

            ExerciseEntry.objects.bulk_create(exercise_instances)

            self.stdout.write(
                self.style.SUCCESS("Successfully populated exercise database")
            )

        except requests.exceptions.RequestException as e:
            self.stderr.write(e)
