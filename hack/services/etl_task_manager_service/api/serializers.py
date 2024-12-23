from rest_framework import serializers
from .models import EtlTask, TaskRun


class TaskRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRun
        fields = ['id', 'etl_task', 'state', 'run_at', 'extracted_data_count']


class EtlTaskSerializer(serializers.ModelSerializer):
    runs = TaskRunSerializer(many=True, read_only=True)

    class Meta:
        model = EtlTask
        fields = [
            'id',
            'released',
            'extraction_script',
            'field_rules',
            'anonymization_rules',
            'transformation_scripts',
            'uploading_script',
            'runs'
        ]
