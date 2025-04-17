# Generated by Django 5.1.7 on 2025-04-17 15:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trajectories', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Trajectory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pace_type', models.CharField(choices=[('DAILY', 'Daily'), ('WEEKLY', 'Weekly'), ('MONTHLY', 'Monthly'), ('YEARLY', 'Yearly')], max_length=50)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('target_date', models.DateField(verbose_name='Target Date')),
                ('amount', models.IntegerField()),
                ('objective', models.CharField(choices=[('INCREASE', 'Increase'), ('DECREASE', 'Decrease'), ('SAME', 'Same')], max_length=50)),
                ('goal_type', models.CharField(choices=[('FOOD', 'Food'), ('EXERCISE', 'Exercise')], max_length=10)),
                ('focus_area', models.TextField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
