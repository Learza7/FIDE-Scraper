# Generated by Django 4.0.5 on 2022-06-21 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0002_alter_person_birth_date_alter_person_blitz_elo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='birth date'),
        ),
    ]