# Generated by Django 2.2.4 on 2019-09-21 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('testweb', '0007_auto_20190920_1543'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='modulestruct',
            options={'ordering': ['struct_sort']},
        ),
    ]
