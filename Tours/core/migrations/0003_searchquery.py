# Generated by Django 5.1.6 on 2025-03-04 22:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_category_island_sitevisit_type_booking_category_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="SearchQuery",
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
                ("query", models.TextField()),
                ("count", models.IntegerField(default=0)),
                (
                    "island",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.island"
                    ),
                ),
            ],
        ),
    ]
