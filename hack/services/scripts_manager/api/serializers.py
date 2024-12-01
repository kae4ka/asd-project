from rest_framework import serializers
from .models import Script, Field, FieldRule, AnonymizationRule, TransformationScript

class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = ['ext_datamodule_id', 'field_name']
        extra_kwargs = {
            'ext_datamodule_id': {'help_text': 'ID внешнего датамодуля'},
            'field_name': {'help_text': 'Название поля'}
        }

class FieldRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldRule
        fields = ['default_value', 'min_value', 'max_value', 'field_type', 'type']
        extra_kwargs = {
            'default_value': {'help_text': 'Значение по умолчанию'},
            'min_value': {'help_text': 'Минимальное допустимое значение'},
            'max_value': {'help_text': 'Максимальное допустимое значение'},
            'field_type': {'help_text': 'Тип поля'},
            'type': {'help_text': 'Тип правила'}
        }

class AnonymizationRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnonymizationRule
        fields = ['type']
        extra_kwargs = {
            'type': {'help_text': 'Тип правила анонимизации'}
        }

class TransformationScriptSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransformationScript
        fields = ['transformation_script', 'type']
        extra_kwargs = {
            'transformation_script': {'help_text': 'Скрипт трансформации'},
            'type': {'help_text': 'Тип трансформации'}
        }

class ScriptSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True, required=False, help_text="Список полей, связанных со скриптом")
    field_rule = FieldRuleSerializer(required=False, help_text="Правила полей")
    anonymization_rule = AnonymizationRuleSerializer(required=False, help_text="Правила анонимизации")
    transformation_script = TransformationScriptSerializer(required=False, help_text="Скрипт трансформации")

    class Meta:
        model = Script
        fields = ['id', 'task_id', 'fields', 'released', 'script_type', 'content',
                  'field_rule', 'anonymization_rule', 'transformation_script']
        extra_kwargs = {
            'task_id': {'help_text': 'ID ETL-задания'},
            'released': {'help_text': 'Флаг релиза скрипта'},
            'script_type': {'help_text': 'Тип скрипта'},
            'content': {'help_text': 'Содержимое скрипта'}
        }

    def create(self, validated_data):
        fields_data = validated_data.pop('fields', [])
        field_rule_data = validated_data.pop('field_rule', None)
        anonymization_rule_data = validated_data.pop('anonymization_rule', None)
        transformation_script_data = validated_data.pop('transformation_script', None)

        script = Script.objects.create(**validated_data)

        for field_data in fields_data:
            Field.objects.create(script=script, **field_data)

        if field_rule_data:
            FieldRule.objects.create(script=script, **field_rule_data)

        if anonymization_rule_data:
            AnonymizationRule.objects.create(script=script, **anonymization_rule_data)

        if transformation_script_data:
            TransformationScript.objects.create(script=script, **transformation_script_data)

        return script

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields', None)
        field_rule_data = validated_data.pop('field_rule', None)
        anonymization_rule_data = validated_data.pop('anonymization_rule', None)
        transformation_script_data = validated_data.pop('transformation_script', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if fields_data is not None:
            instance.fields.all().delete()
            for field_data in fields_data:
                Field.objects.create(script=instance, **field_data)

        if field_rule_data is not None:
            FieldRule.objects.update_or_create(script=instance, defaults=field_rule_data)

        if anonymization_rule_data is not None:
            AnonymizationRule.objects.update_or_create(script=instance, defaults=anonymization_rule_data)

        if transformation_script_data is not None:
            TransformationScript.objects.update_or_create(script=instance, defaults=transformation_script_data)

        return instance
