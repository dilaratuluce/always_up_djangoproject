# Generated by Django 4.0.6 on 2022-08-11 08:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_logged_in_app', '0017_alter_todo_priority_alter_todo_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='date',
            field=models.DateField(choices=[(datetime.date(2022, 8, 11), datetime.date(2022, 8, 11)), (datetime.date(2022, 8, 12), datetime.date(2022, 8, 12)), (datetime.date(2022, 8, 13), datetime.date(2022, 8, 13)), (datetime.date(2022, 8, 14), datetime.date(2022, 8, 14)), (datetime.date(2022, 8, 15), datetime.date(2022, 8, 15)), (datetime.date(2022, 8, 16), datetime.date(2022, 8, 16)), (datetime.date(2022, 8, 17), datetime.date(2022, 8, 17))], default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='todo',
            name='priority',
            field=models.TextField(choices=[('low', 'Low'), ('normal', 'Normal'), ('high', 'High'), ('very_high', 'Very high')], default='normal'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]