# Generated by Django 4.1.7 on 2023-04-07 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0023_rename_accountbalance_useraccount_account_balance_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transfer',
            old_name='recipient_account',
            new_name='receiver_account',
        ),
    ]