# Generated by Django 4.0.6 on 2022-07-29 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo_logged_in_app', '0009_alter_todo_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='todo',
            name='date',
        ),
    ]
