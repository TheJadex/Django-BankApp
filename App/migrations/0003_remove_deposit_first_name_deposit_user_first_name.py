# Generated by Django 4.1.7 on 2023-04-01 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_deposit_first_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deposit',
            name='first_name',
        ),
        migrations.AddField(
            model_name='deposit',
            name='user_first_name',
            field=models.CharField(default='first_name', max_length=30),
            preserve_default=False,
        ),
    ]