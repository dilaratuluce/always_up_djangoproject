# Generated by Django 4.0.6 on 2022-08-10 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo_logged_in_app', '0017_alter_todo_priority_alter_todo_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]