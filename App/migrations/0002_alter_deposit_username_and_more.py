# Generated by Django 4.1.7 on 2023-10-09 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deposit',
            name='username',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='sender_username',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='account_number',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='username',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
