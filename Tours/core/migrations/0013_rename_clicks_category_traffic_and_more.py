# Generated by Django 5.1.6 on 2025-03-06 20:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0012_alter_booking_category"),
    ]

    operations = [
        migrations.RenameField(
            model_name="category",
            old_name="clicks",
            new_name="traffic",
        ),
        migrations.RenameField(
            model_name="island",
            old_name="clicks",
            new_name="traffic",
        ),
    ]
