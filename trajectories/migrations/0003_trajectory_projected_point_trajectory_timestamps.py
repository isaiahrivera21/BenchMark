# Generated by Django 5.1.7 on 2025-04-18 18:06

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trajectories", "0002_trajectory_delete_question"),
    ]

    operations = [
        migrations.AddField(
            model_name="trajectory",
            name="projected_point",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.FloatField(),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="trajectory",
            name="timestamps",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.DateTimeField(),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        ),
    ]
