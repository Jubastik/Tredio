# Generated by Django 4.0.4 on 2022-05-19 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='rank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.rank', verbose_name='Ранг'),
        ),
    ]