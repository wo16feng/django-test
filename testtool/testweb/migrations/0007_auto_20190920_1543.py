# Generated by Django 2.2.4 on 2019-09-20 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testweb', '0006_auto_20190920_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moduledatatype',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False),
        ),
    ]
