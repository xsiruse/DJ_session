# Generated by Django 2.1.1 on 2020-01-14 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='seession_id',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
