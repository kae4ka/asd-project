from django.db import models


class UserRole(models.IntegerChoices):
    EDIT_TASK = 0, 'Edit Task'
    MANAGE_DATA = 1, 'Manage Data'
    CREATE_EXT_DATAMODULE = 2, 'Create Ext Datamodule'
    PROCESS_ETL_TASK = 3, 'Process ETL Task'
    UNKNOWN = 4, 'Unknown'


class ExtDatamoduleAccessType(models.IntegerChoices):
    READ = 0, 'Read'
    WRITE = 1, 'Write'
    OWNER = 2, 'Owner'


class User(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=150)
    roles = models.ManyToManyField('Role', related_name='users')
    ext_datamodule_accesses = models.ManyToManyField('ExtDatamoduleAccess', related_name='users')


class Role(models.Model):
    id = models.AutoField(primary_key=True)
    role = models.IntegerField(choices=UserRole.choices, unique=True, default=UserRole.UNKNOWN)

    def __str__(self):
        return self.get_role_display()


class ExtDatamoduleAccess(models.Model):
    id = models.AutoField(primary_key=True)
    ext_datamodule_id = models.CharField(max_length=100, default="0")
    access_types = models.ManyToManyField('AccessType')
    approved = models.BooleanField(null=True)


class AccessType(models.Model):
    access_type = models.IntegerField(choices=ExtDatamoduleAccessType.choices)

    def __str__(self):
        return self.get_access_type_display()