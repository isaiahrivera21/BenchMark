# Generated by Django 5.1.7 on 2025-04-18 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("trajectories", "0006_rename_projected_point_trajectory_projected_points"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trajectory",
            name="current_amount",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="trajectory",
            name="future_amount",
            field=models.IntegerField(),
        ),
    ]
