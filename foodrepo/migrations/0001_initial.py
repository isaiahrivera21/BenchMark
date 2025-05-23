# Generated by Django 5.1.7 on 2025-03-28 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FoodEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("food_name", models.CharField(max_length=200)),
                ("calories", models.IntegerField()),
                ("fat", models.IntegerField(blank=True, null=True)),
                ("carbohydrates", models.IntegerField(blank=True, null=True)),
                ("protien", models.IntegerField(blank=True, null=True)),
                ("cholestorol", models.IntegerField(blank=True, null=True)),
                ("sodium", models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
