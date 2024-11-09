# Generated by Django 4.1.5 on 2024-10-27 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_reviewrating_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewrating',
            name='positive_probab',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reviewrating',
            name='review',
            field=models.TextField(blank=True, max_length=700),
        ),
    ]