# Generated by Django 5.1.3 on 2024-12-01 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_user_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_type', models.IntegerField(choices=[(0, 'Read'), (1, 'Write'), (2, 'Owner')])),
            ],
        ),
        migrations.RemoveField(
            model_name='extdatamoduleaccess',
            name='access_type',
        ),
        migrations.RemoveField(
            model_name='extdatamoduleaccess',
            name='ext_datamodule',
        ),
        migrations.RemoveField(
            model_name='extdatamoduleaccess',
            name='user',
        ),
        migrations.RemoveField(
            model_name='role',
            name='name',
        ),
        migrations.AddField(
            model_name='extdatamoduleaccess',
            name='ext_datamodule_id',
            field=models.CharField(default='0', max_length=100),
        ),
        migrations.AddField(
            model_name='role',
            name='role',
            field=models.IntegerField(choices=[(0, 'Edit Task'), (1, 'Manage Data'), (2, 'Create Ext Datamodule'), (3, 'Process ETL Task'), (4, 'Unknown')], default=4, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='ext_datamodule_accesses',
            field=models.ManyToManyField(related_name='users', to='api.extdatamoduleaccess'),
        ),
        migrations.AlterField(
            model_name='extdatamoduleaccess',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='role',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(max_length=100, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.CreateModel(
            name='AccessRequest',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('state', models.BooleanField(null=True)),
                ('ext_datamodule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.extdatamoduleaccess')),
                ('owner_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_requests', to='api.user')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.user')),
            ],
        ),
        migrations.AddField(
            model_name='extdatamoduleaccess',
            name='access_types',
            field=models.ManyToManyField(to='api.accesstype'),
        ),
    ]