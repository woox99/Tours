# Generated by Django 5.1.6 on 2025-03-21 21:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=50, unique=True)),
                ("is_popular", models.BooleanField(default=False)),
                ("traffic", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Island",
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
                ("name", models.CharField(max_length=50, unique=True)),
                ("modified", models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name="SiteVisit",
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
                ("created", models.DateTimeField(auto_now_add=True)),
                ("ref", models.CharField(default=None, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Type",
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
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Booking",
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
                ("title", models.CharField(max_length=100)),
                ("company_name", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("is_public", models.BooleanField(default=False)),
                ("is_verified", models.BooleanField(default=False)),
                ("is_popular", models.BooleanField(default=False)),
                ("fh_id", models.IntegerField()),
                ("referral_link", models.URLField()),
                ("image_URL", models.URLField()),
                ("weight", models.IntegerField(default=2500)),
                ("modified", models.DateTimeField(auto_now=True)),
                (
                    "tags",
                    models.ManyToManyField(related_name="bookings", to="core.category"),
                ),
                (
                    "island",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.island"
                    ),
                ),
            ],
        ),
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
                ("count", models.IntegerField(default=1)),
                ("results", models.IntegerField(default=1)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "island",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.island"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="category",
            name="type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="core.type"
            ),
        ),
    ]
