# Generated by Django 3.2.4 on 2021-07-31 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wish', '0002_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
