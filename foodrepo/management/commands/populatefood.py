from django.core.management.base import BaseCommand, CommandError
from foodrepo.models import FoodEntry
from dotenv import load_dotenv
import os
import requests
from django.db import transaction

NUTRIENT_MAPPING = {
    "Energy": "calories",
    "Total lipid (fat)": "fat",
    "Carbohydrate, by difference": "carbohydrates",
    "Protein": "protein",
    "Cholesterol": "cholesterol",
    "Sodium, Na": "sodium",
    "Total Sugars": "sugars",
}


class Command(BaseCommand):
    help = "Populates food database from USDA API"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to pull data from USDA API...")

        load_dotenv()
        api_key = os.getenv("USDA_API_KEY")
        base_url = "https://api.nal.usda.gov/fdc/v1/search"

        page = 1
        max_pages = 3
        page_size = 50
        all_food_instances = []

        try:
            while page <= max_pages:
                self.stdout.write(f"Processing page {page}/{max_pages}...")

                params = {
                    "query": "",
                    "pageSize": page_size,
                    "pageNumber": page,
                    "api_key": api_key,
                }

                response = requests.get(base_url, params=params)
                if not response.ok:
                    self.stderr.write(
                        f"API Error: {response.status_code} - {response.text}"
                    )
                    page += 1
                    continue

                data = response.json()
                foods = data.get("foods", [])

                if not foods:
                    self.stdout.write("No more foods found, stopping pagination.")
                    break

                food_instances = []
                for food in foods:
                    try:
                        nutrients = {}
                        for nutrient in food.get("foodNutrients", []):
                            name = nutrient.get("nutrientName")

                            value = nutrient.get("value")

                            if name in NUTRIENT_MAPPING and value is not None:

                                nutrients[NUTRIENT_MAPPING[name]] = value

                        if not nutrients.get("calories"):
                            self.stdout.write(
                                f"Skipping {food.get('description')} - missing calories"
                            )
                            continue

                        food_instances.append(
                            FoodEntry(
                                food_name=food.get("description", "Unknown Food"),
                                calories=nutrients["calories"],
                                fat=nutrients.get("fat", 0),
                                carbohydrates=nutrients.get("carbohydrates", 0),
                                protein=nutrients.get("protein", 0),
                                cholesterol=nutrients.get("cholesterol", 0),
                                sodium=nutrients.get("sodium", 0),
                                sugar=nutrients.get("sugars", 0),
                            )
                        )

                    except Exception as e:
                        self.stderr.write(
                            f"Error processing food {food.get('fdcId')}: {str(e)}"
                        )
                        continue

                all_food_instances.extend(food_instances)
                self.stdout.write(
                    f"Page {page}: Added {len(food_instances)} valid entries"
                )
                page += 1

            with transaction.atomic():
                created_count = len(
                    FoodEntry.objects.bulk_create(
                        all_food_instances, ignore_conflicts=True
                    )
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully added {created_count} food entries. "
                    f"Skipped {len(all_food_instances) - created_count} duplicates."
                )
            )

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Fatal error: {str(e)}"))
            raise CommandError("Database population aborted")
