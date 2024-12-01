from rest_framework import serializers
from .models import User, Role, ExtDatamoduleAccess, AccessType


class AccessTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessType
        fields = ['access_type']


class ExtDatamoduleAccessSerializer(serializers.ModelSerializer):
    access_types = AccessTypeSerializer(many=True)

    class Meta:
        model = ExtDatamoduleAccess
        fields = ['id', 'ext_datamodule_id', 'access_types', 'approved']


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['role']


class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    ext_datamodule_accesses = ExtDatamoduleAccessSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'name', 'roles', 'ext_datamodule_accesses']

