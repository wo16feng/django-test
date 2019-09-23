# Generated by Django 2.2.4 on 2019-09-18 02:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleCode',
            fields=[
                ('code_id', models.IntegerField(primary_key=True, serialize=False)),
                ('code_name', models.CharField(max_length=32)),
                ('code_des', models.CharField(max_length=64)),
            ],
            options={
                'db_table': 'ModuleCode',
            },
        ),
        migrations.CreateModel(
            name='ModuleDataType',
            fields=[
                ('id', models.PositiveIntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('struct_id', models.PositiveIntegerField(default=0)),
                ('name', models.CharField(default='', max_length=32)),
                ('module_id', models.PositiveIntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'db_table': 'ModuleDataType',
            },
        ),
        migrations.CreateModel(
            name='ModuleName',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('des', models.CharField(max_length=64, null=True)),
            ],
            options={
                'db_table': 'ModuleName',
            },
        ),
        migrations.CreateModel(
            name='ModuleRspd',
            fields=[
                ('word_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('word_name', models.CharField(max_length=16)),
                ('word_struct', models.BooleanField(default=False)),
                ('word_type', models.CharField(max_length=8)),
                ('word_sort', models.IntegerField(default=0)),
                ('word_content', models.CharField(max_length=32)),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testweb.ModuleCode')),
            ],
            options={
                'db_table': 'ModuleRspd',
                'ordering': ['word_sort'],
            },
        ),
        migrations.CreateModel(
            name='ModuleRqst',
            fields=[
                ('word_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('word_name', models.CharField(max_length=16)),
                ('word_struct', models.BooleanField(default=False)),
                ('word_type', models.CharField(max_length=8)),
                ('word_sort', models.IntegerField(default=0)),
                ('word_content', models.CharField(max_length=32)),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testweb.ModuleCode')),
            ],
            options={
                'db_table': 'ModuleRqst',
                'ordering': ['word_sort'],
            },
        ),
        migrations.AddField(
            model_name='modulecode',
            name='classes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='testweb.ModuleName'),
        ),
        migrations.CreateModel(
            name='AddressInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='地址')),
                ('pid', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='testweb.AddressInfo', verbose_name='自关联')),
            ],
            options={
                'verbose_name': '省市县地址信息',
                'verbose_name_plural': '省市县地址信息',
                'db_table': 'AddressInfo',
            },
        ),
    ]
