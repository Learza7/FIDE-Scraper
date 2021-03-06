# Generated by Django 4.0.5 on 2022-06-21 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Models', '0003_alter_person_birth_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='blitz_elo',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='continental_rank',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='national_rank',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='rapid_elo',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='standard_elo',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='world_rank',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
