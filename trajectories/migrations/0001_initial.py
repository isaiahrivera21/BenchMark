# Generated by Django 5.1.7 on 2025-03-14 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('pace_type', models.CharField(choices=[('DAILY', 'Daily'), ('WEEKLY', 'Weekly'), ('MONTHLY', 'Monthly'), ('YEARLY', 'Yearly')], max_length=50)),
                ('cur_value', models.IntegerField()),
                ('goal_value', models.IntegerField()),
                ('improvement', models.FloatField()),
                ('target_date', models.DateField(verbose_name='target date')),
            ],
        ),
    ]
