# Generated by Django 4.0.6 on 2022-08-17 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_logged_in_app', '0025_rename_todocatagory_todocategory_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='priority',
            field=models.TextField(choices=[('very_low', 'Very Low'), ('low', 'Low'), ('normal', 'Normal'), ('high', 'High'), ('very_high', 'Very high')], default='normal'),
        ),
    ]
