# Generated by Django 4.0.4 on 2022-05-11 05:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("rating", "0001_initial"),
        ("users", "0001_initial"),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="City",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("query", models.CharField(max_length=250)),
                ("fias", models.CharField(max_length=50)),
                ("city", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="theatres.city")),
            ],
        ),
        migrations.CreateModel(
            name="Troupe",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ],
        ),
        migrations.CreateModel(
            name="TroupeMember",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("role", models.CharField(blank=True, max_length=100, null=True)),
                ("profile", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="users.profile")),
                ("troupe_id", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="theatres.troupe")),
            ],
        ),
        migrations.CreateModel(
            name="Theatre",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                (
                    "contacts",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="core.contactsgroup"
                    ),
                ),
                ("location", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="theatres.location")),
                (
                    "reviews",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="rating.reviewgroup"
                    ),
                ),
                (
                    "troupe",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="theatres.troupe"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=150)),
                (
                    "reviews",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="rating.reviewgroup"
                    ),
                ),
                ("theatre", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="theatres.theatre")),
                (
                    "troupe",
                    models.ForeignKey(
                        blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="theatres.troupe"
                    ),
                ),
            ],
        ),
    ]
