# Generated by Django 5.1.6 on 2025-03-05 22:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_searchquery_results"),
    ]

    operations = [
        migrations.DeleteModel(
            name="SearchQuery",
        ),
    ]
