# Generated by Django 5.1.3 on 2024-12-01 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_accesstype_remove_extdatamoduleaccess_access_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extdatamodule',
            name='owners',
        ),
        migrations.AddField(
            model_name='extdatamoduleaccess',
            name='approved',
            field=models.BooleanField(null=True),
        ),
        migrations.DeleteModel(
            name='AccessRequest',
        ),
        migrations.DeleteModel(
            name='ExtDatamodule',
        ),
    ]
