# Generated by Django 4.0.1 on 2022-01-28 23:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_room_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='topic',
            new_name='name',
        ),
    ]
