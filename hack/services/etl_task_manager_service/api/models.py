from django.db import models
from django.utils import timezone


class TaskRunState(models.TextChoices):
    RUNNING = 'Running', 'Running'
    PAUSED = 'Paused', 'Paused'
    STOPPED = 'Stopped', 'Stopped'


class EtlTask(models.Model):
    id = models.CharField(primary_key=True, max_length=100)  # Будем вручную задавать
    released = models.BooleanField(default=False)
    extraction_script = models.TextField(blank=True, null=True)
    # field_rules, anonymization_rules, transformation_scripts храним в JSON
    field_rules = models.JSONField(default=list, blank=True)
    anonymization_rules = models.JSONField(default=list, blank=True)
    transformation_scripts = models.JSONField(default=list, blank=True)
    uploading_script = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"ETL Task: {self.id}"


class TaskRun(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    etl_task = models.ForeignKey(EtlTask, related_name='runs', on_delete=models.CASCADE)
    state = models.CharField(max_length=20, choices=TaskRunState.choices, default=TaskRunState.RUNNING)
    run_at = models.DateTimeField(default=timezone.now)
    extracted_data_count = models.BigIntegerField(default=0)

    def __str__(self):
        return f"TaskRun {self.id} for ETL Task {self.etl_task.id}"
