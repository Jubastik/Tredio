# Generated by Django 4.0.4 on 2022-05-24 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("theatres", "0006_event_is_published_theatre_is_published"),
    ]

    operations = [
        migrations.CreateModel(
            name="ModerationEvent",
            fields=[],
            options={
                "verbose_name": "Событие на модерации",
                "verbose_name_plural": "События на модерации",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("theatres.event",),
        ),
        migrations.CreateModel(
            name="ModerationTheatre",
            fields=[],
            options={
                "verbose_name": "Театр на модерации",
                "verbose_name_plural": "Театры на модерации",
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("theatres.theatre",),
        ),
    ]
