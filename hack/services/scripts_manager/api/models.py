from django.db import models
from django.utils import timezone


class Script(models.Model):
    SCRIPT_TYPES = [
        ('extractor', 'Extractor'),
        ('field_rule', 'Field Rule'),
        ('anonymization_rule', 'Anonymization Rule'),
        ('transformer', 'Transformation Script'),
        ('uploader', 'Uploader'),
    ]

    id = models.AutoField(primary_key=True)
    task_id = models.CharField(max_length=255)
    released = models.BooleanField(default=False)
    script_type = models.CharField(max_length=50, choices=SCRIPT_TYPES)
    content = models.TextField()  # Содержимое скрипта
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.script_type} - {self.id}"


class Field(models.Model):
    script = models.ForeignKey(Script, related_name='fields', on_delete=models.CASCADE, null=True)
    ext_datamodule_id = models.CharField(max_length=255)
    field_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.field_name} ({self.ext_datamodule_id})"


class FieldRule(models.Model):
    FIELD_TYPES = [
        ('Integer', 'Integer'),
        ('String', 'String'),
        ('Double', 'Double'),
    ]

    RULE_TYPES = [
        ('FillEmpty', 'Fill Empty'),
        ('IgnoreEmpty', 'Ignore Empty'),
        ('RemoveEmpty', 'Remove Empty'),
        ('FillOutOfRange', 'Fill Out of Range'),
        ('IgnoreOutOfRange', 'Ignore Out of Range'),
        ('RemoveOutOfRange', 'Remove Out of Range'),
    ]

    script = models.OneToOneField(Script, on_delete=models.CASCADE, related_name='field_rule', null=True)
    default_value = models.CharField(max_length=255, blank=True, null=True)
    min_value = models.CharField(max_length=255, blank=True, null=True)
    max_value = models.CharField(max_length=255, blank=True, null=True)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES)
    type = models.CharField(max_length=50, choices=RULE_TYPES)

    def __str__(self):
        return f"FieldRule for {self.script.id}"


class AnonymizationRule(models.Model):
    RULE_TYPES = [
        ('Generalization', 'Generalization'),
        ('Suppression', 'Suppression'),
        ('Anatomization', 'Anatomization'),
        ('Permutation', 'Permutation'),
        ('Perturbation', 'Perturbation'),
    ]

    script = models.OneToOneField(Script, on_delete=models.CASCADE, related_name='anonymization_rule', null=True)
    type = models.CharField(max_length=50, choices=RULE_TYPES)

    def __str__(self):
        return f"AnonymizationRule for {self.script.id}"


class TransformationScript(models.Model):
    TRANSFORMATION_TYPES = [
        ('Merge', 'Merge'),
        ('Update', 'Update'),
    ]

    script = models.OneToOneField(Script, on_delete=models.CASCADE, related_name='transformation_script', null=True)
    transformation_script = models.TextField()
    type = models.CharField(max_length=50, choices=TRANSFORMATION_TYPES)

    def __str__(self):
        return f"TransformationScript for {self.script.id}"
