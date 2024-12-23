import requests
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.conf import settings
from .models import EtlTask, TaskRun, TaskRunState
from .serializers import EtlTaskSerializer, TaskRunSerializer


class EtlTaskManagerViewSet(viewsets.ViewSet):
    """
    ViewSet для управления ETL Task согласно ProtoContract.
    """

    USER_MANAGER_URL = 'http://84.201.148.234/etl-express-project/user_manager/api/get_user/{user_id}/'

    def check_user_access(self, user_id):
        """
        Проверка доступа пользователя через User Manager.
        """
        if not user_id:
            return False
        try:
            response = requests.get(
                self.USER_MANAGER_URL.format(user_id=user_id),
                headers={'accept': 'application/json'},
                timeout=5
            )
            if response.status_code == 200:
                # Дополнительная логика проверки ролей, если требуется
                return True
            else:
                return False
        except requests.RequestException:
            return False

    def get_user_id(self, request):
        """
        Извлекает user_id из заголовка X-USER-ID
        """
        return request.headers.get('X-USER-ID')

    # --------------------------------------------------
    # 1. CreateTask -> POST /create
    # --------------------------------------------------
    @swagger_auto_schema(
        operation_description="Создание новой задачи (CreateTask).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_id': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="ID задачи (обязательный параметр)"
                )
            },
            required=['task_id']
        ),
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя (для проверки в User Manager).",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            201: openapi.Response(
                description="Задача успешно создана.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'result': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True)
                    }
                )
            ),
            400: openapi.Response(description="Неверные параметры (не передан task_id и т.д.)."),
            401: openapi.Response(description="Нет прав доступа (Unauthorized).")
        }
    )
    @action(detail=False, methods=['post'], url_path='create')
    def create_task(self, request):
        """
        Создание новой задачи (CreateTask).
        """
        user_id = self.get_user_id(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        task_id = request.data.get('task_id', None)
        if not task_id:
            return Response({'error': 'No task_id provided'}, status=status.HTTP_400_BAD_REQUEST)

        EtlTask.objects.create(id=task_id)
        return Response({'result': True}, status=status.HTTP_201_CREATED)

    # --------------------------------------------------
    # 2. GetTask -> GET /get/<task_id> (или POST /get/{task_id})
    # --------------------------------------------------
    @swagger_auto_schema(
        operation_description="Получение информации о задаче (GetTask).",
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя (для проверки в User Manager).",
                type=openapi.TYPE_STRING,
                required=True
            ),
            openapi.Parameter(
                'task_id',
                openapi.IN_PATH,
                description="ID задачи для получения информации.",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Информация о задаче.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'task': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Данные модели EtlTask"
                        )
                    }
                )
            ),
            401: openapi.Response(description="Нет прав доступа (Unauthorized)."),
            404: openapi.Response(description="Задача не найдена.")
        }
    )
    @action(detail=False, methods=['get'], url_path=r'get/(?P<task_id>[^/.]+)')
    def get_task(self, request, task_id=None):
        """
        Получение информации о задаче (GetTask).
        """
        user_id = self.get_user_id(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        task = get_object_or_404(EtlTask, pk=task_id)
        serializer = EtlTaskSerializer(task)
        return Response({'task': serializer.data}, status=status.HTTP_200_OK)

    # --------------------------------------------------
    # 3. GetAllTask -> GET /get-all
    # --------------------------------------------------
    @swagger_auto_schema(
        operation_description="Получение списка всех задач (GetAll).",
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя (для проверки в User Manager).",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Список всех ETL-задач.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'tasks': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_OBJECT),
                            description="Массив объектов EtlTask."
                        )
                    }
                )
            ),
            401: openapi.Response(description="Нет прав доступа (Unauthorized).")
        }
    )
    @action(detail=False, methods=['get'], url_path='get-all')
    def get_all_tasks(self, request):
        """
        Получение списка всех задач (GetAll).
        """
        user_id = self.get_user_id(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        tasks = EtlTask.objects.all()
        serializer = EtlTaskSerializer(tasks, many=True)
        return Response({'tasks': serializer.data}, status=status.HTTP_200_OK)

    # --------------------------------------------------
    # 4. UpdateExtractionScript -> PUT /update/script/extraction
    # --------------------------------------------------
    @swagger_auto_schema(
        operation_description="Обновление extraction_script (UpdateExtractionScript).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID задачи'),
                'script_id': openapi.Schema(type=openapi.TYPE_STRING, description='Опционально ID скрипта'),
                'extraction_script': openapi.Schema(type=openapi.TYPE_STRING, description='Содержимое скрипта извлечения')
            }
        ),
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя (для проверки в User Manager).",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(description="Скрипт успешно обновлён."),
            400: openapi.Response(description="Неверные параметры."),
            401: openapi.Response(description="Нет прав доступа.")
        }
    )
    @action(detail=False, methods=['put'], url_path='update/script/extraction')
    def update_extraction_script(self, request):
        """
        Обновление extraction_script (UpdateExtractionScript).
        """
        user_id = self.get_user_id(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        task_id = request.data.get('task_id')
        script_id = request.data.get('script_id', None)
        if not task_id:
            return Response({'error': 'No task_id provided'}, status=status.HTTP_400_BAD_REQUEST)

        extraction_content = request.data.get('extraction_script', '')
        task = get_object_or_404(EtlTask, pk=task_id)
        task.extraction_script = extraction_content
        task.save()
        return Response({'result': True}, status=status.HTTP_200_OK)

    # --------------------------------------------------
    # 5. UpdateFieldRules -> PUT /update/script/field_rules
    # --------------------------------------------------
    @swagger_auto_schema(
        operation_description="Обновление field_rules (UpdateFieldRules).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID задачи'),
                'rules_to_add': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description='Правила для добавления'
                ),
                'rules_to_remove': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description='Правила для удаления'
                )
            }
        ),
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя (для проверки в User Manager).",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(description="Field rules успешно обновлены."),
            400: openapi.Response(description="Неверные параметры."),
            401: openapi.Response(description="Нет прав доступа.")
        }
    )
    @action(detail=False, methods=['put'], url_path='update/script/field_rules')
    def update_field_rules(self, request):
        """
        Обновление field_rules (UpdateFieldRules).
        """
        user_id = self.get_user_id(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        task_id = request.data.get('task_id')
        if not task_id:
            return Response({'error': 'No task_id provided'}, status=status.HTTP_400_BAD_REQUEST)

        rules_to_add = request.data.get('rules_to_add', [])
        rules_to_remove = request.data.get('rules_to_remove', [])

        task = get_object_or_404(EtlTask, pk=task_id)
        current_rules = task.field_rules
        updated_rules = set(current_rules).union(set(rules_to_add)) - set(rules_to_remove)
        task.field_rules = list(updated_rules)
        task.save()
        return Response({'result': True}, status=status.HTTP_200_OK)

    # --------------------------------------------------
    # 6. UpdateAnonymizationRules -> PUT /update/script/anomyziation
    # --------------------------------------------------
    @swagger_auto_schema(
        operation_description="Обновление anonymization_rules (UpdateAnonymizationRules).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID задачи'),
                'rules_to_add': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description='Правила анонимизации для добавления'
                ),
                'rules_to_remove': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description='Правила анонимизации для удаления'
                )
            }
        ),
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя (для проверки в User Manager).",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(description="Anonymization rules успешно обновлены."),
            400: openapi.Response(description="Неверные параметры."),
            401: openapi.Response(description="Нет прав доступа.")
        }
    )
    @action(detail=False, methods=['put'], url_path='update/script/anomyziation')
    def update_anonymization_rules(self, request):
        """
        Обновление anonymization_rules (UpdateAnonymizationRules).
        """
        user_id = self.get_user_id(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        task_id = request.data.get('task_id')
        if not task_id:
            return Response({'error': 'No task_id provided'}, status=status.HTTP_400_BAD_REQUEST)

        rules_to_add = request.data.get('rules_to_add', [])
        rules_to_remove = request.data.get('rules_to_remove', [])

        task = get_object_or_404(EtlTask, pk=task_id)
        current_rules = task.anonymization_rules
        updated_rules = set(current_rules).union(set(rules_to_add)) - set(rules_to_remove)
        task.anonymization_rules = list(updated_rules)
        task.save()
        return Response({'result': True}, status=status.HTTP_200_OK)

    # --------------------------------------------------
    # 7. UpdateTransformationScripts -> PUT /update/script/transformation
    # --------------------------------------------------
    @swagger_auto_schema(
        operation_description="Обновление transformation_scripts (UpdateTransformationScripts).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID задачи'),
                'scripts_to_add': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description='Скрипты трансформации для добавления'
                ),
                'scripts_to_remove': openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(type=openapi.TYPE_STRING),
                    description='Скрипты трансформации для удаления'
                )
            }
        ),
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя (для проверки в User Manager).",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(description="Transformation scripts успешно обновлены."),
            400: openapi.Response(description="Неверные параметры."),
            401: openapi.Response(description="Нет прав доступа.")
        }
    )
    @action(detail=False, methods=['put'], url_path='update/script/transformation')
    def update_transformation_scripts(self, request):
        """
        Обновление transformation_scripts (UpdateTransformationScripts).
        """
        user_id = self.get_user_id(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        task_id = request.data.get('task_id')
        if not task_id:
            return Response({'error': 'No task_id provided'}, status=status.HTTP_400_BAD_REQUEST)

        scripts_to_add = request.data.get('scripts_to_add', [])
        scripts_to_remove = request.data.get('scripts_to_remove', [])

        task = get_object_or_404(EtlTask, pk=task_id)
        current_scripts = task.transformation_scripts
        updated_scripts = set(current_scripts).union(set(scripts_to_add)) - set(scripts_to_remove)
        task.transformation_scripts = list(updated_scripts)
        task.save()
        return Response({'result': True}, status=status.HTTP_200_OK)

    # --------------------------------------------------
    # 8. UpdateUploadingScript -> PUT /update/script/uploading
    # --------------------------------------------------
    @swagger_auto_schema(
        operation_description="Обновление uploading_script (UpdateUploadingScript).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID задачи'),
                'script_id': openapi.Schema(type=openapi.TYPE_STRING, description='Содержимое скрипта загрузки или его ID')
            }
        ),
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя (для проверки в User Manager).",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(description="Uploading script успешно обновлён."),
            400: openapi.Response(description="Неверные параметры."),
            401: openapi.Response(description="Нет прав доступа.")
        }
    )
    @action(detail=False, methods=['put'], url_path='update/script/uploading')
    def update_uploading_script(self, request):
        """
        Обновление uploading_script (UpdateUploadingScript).
        """
        user_id = self.get_user_id(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        task_id = request.data.get('task_id')
        script_id = request.data.get('script_id')
        if not task_id:
            return Response({'error': 'No task_id provided'}, status=status.HTTP_400_BAD_REQUEST)

        task = get_object_or_404(EtlTask, pk=task_id)
        task.uploading_script = script_id
        task.save()
        return Response({'result': True}, status=status.HTTP_200_OK)

    # --------------------------------------------------
    # 9. Release -> PUT /release
    # --------------------------------------------------
    @swagger_auto_schema(
        operation_description="Ставит released=True у задачи (Release).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID задачи')
            }
        ),
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя (для проверки в User Manager).",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(description="Задача успешно переведена в released=True."),
            400: openapi.Response(description="Неверные параметры."),
            401: openapi.Response(description="Нет прав доступа.")
        }
    )
    @action(detail=False, methods=['put'], url_path='release')
    def release(self, request):
        """
        Ставит released=True у задачи (Release).
        """
        user_id = self.get_user_id(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        task_id = request.data.get('task_id')
        task = get_object_or_404(EtlTask, pk=task_id)
        task.released = True
        task.save()
        return Response({'result': True}, status=status.HTTP_200_OK)

    # --------------------------------------------------
    # 10. Start -> POST /start
    # --------------------------------------------------
    @swagger_auto_schema(
        operation_description="Создаёт новый TaskRun со state=Running (Start).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID задачи'),
                'run_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID запуска'),
            },
            required=['task_id', 'run_id']
        ),
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя (для проверки в User Manager).",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(description="TaskRun создан и запущен."),
            400: openapi.Response(description="Неверные параметры."),
            401: openapi.Response(description="Нет прав доступа.")
        }
    )
    @action(detail=False, methods=['post'], url_path='start')
    def start_task(self, request):
        """
        Создает новый TaskRun (Start).
        """
        user_id = self.get_user_id(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        task_id = request.data.get('task_id')
        run_id = request.data.get('run_id')
        if not all([task_id, run_id]):
            return Response({'error': 'No task_id or run_id provided'}, status=status.HTTP_400_BAD_REQUEST)

        task = get_object_or_404(EtlTask, pk=task_id)
        TaskRun.objects.create(id=run_id, etl_task=task, state=TaskRunState.RUNNING)
        return Response({'result': True}, status=status.HTTP_200_OK)

    # --------------------------------------------------
    # 11. Resume -> POST /resume
    # --------------------------------------------------
    @swagger_auto_schema(
        operation_description="Возобновляет остановленную/приостановленную задачу (Resume).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID задачи'),
                'run_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID запущенного TaskRun')
            },
            required=['task_id', 'run_id']
        ),
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя (для проверки в User Manager).",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(description="TaskRun переведен в состояние Running."),
            400: openapi.Response(description="Неверные параметры."),
            401: openapi.Response(description="Нет прав доступа."),
            404: openapi.Response(description="TaskRun не найден.")
        }
    )
    @action(detail=False, methods=['post'], url_path='resume')
    def resume_task(self, request):
        """
        Возобновляет остановленную/приостановленную задачу (Resume).
        """
        user_id = self.get_user_id(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        task_id = request.data.get('task_id')
        run_id = request.data.get('run_id')
        run = get_object_or_404(TaskRun, pk=run_id, etl_task_id=task_id)
        run.state = TaskRunState.RUNNING
        run.save()
        return Response({'result': True}, status=status.HTTP_200_OK)

    # --------------------------------------------------
    # 12. Pause -> POST /pause
    # --------------------------------------------------
    @swagger_auto_schema(
        operation_description="Приостанавливает задачу (Pause).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID задачи'),
                'run_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID запущенного TaskRun')
            },
            required=['task_id', 'run_id']
        ),
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя (для проверки в User Manager).",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(description="TaskRun переведен в состояние Paused."),
            400: openapi.Response(description="Неверные параметры."),
            401: openapi.Response(description="Нет прав доступа."),
            404: openapi.Response(description="TaskRun не найден.")
        }
    )
    @action(detail=False, methods=['post'], url_path='pause')
    def pause_task(self, request):
        """
        Приостанавливает задачу (Pause).
        """
        user_id = self.get_user_id(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        task_id = request.data.get('task_id')
        run_id = request.data.get('run_id')
        run = get_object_or_404(TaskRun, pk=run_id, etl_task_id=task_id)
        run.state = TaskRunState.PAUSED
        run.save()
        return Response({'result': True}, status=status.HTTP_200_OK)

    # --------------------------------------------------
    # 13. Stop -> POST /stop
    # --------------------------------------------------
    @swagger_auto_schema(
        operation_description="Останавливает задачу (Stop).",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'task_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID задачи'),
                'run_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID запущенного TaskRun')
            },
            required=['task_id', 'run_id']
        ),
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя (для проверки в User Manager).",
                type=openapi.TYPE_STRING,
                required=True
            )
        ],
        responses={
            200: openapi.Response(description="TaskRun переведен в состояние Stopped."),
            400: openapi.Response(description="Неверные параметры."),
            401: openapi.Response(description="Нет прав доступа."),
            404: openapi.Response(description="TaskRun не найден.")
        }
    )
    @action(detail=False, methods=['post'], url_path='stop')
    def stop_task(self, request):
        """
        Останавливает задачу (Stop).
        """
        user_id = self.get_user_id(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        task_id = request.data.get('task_id')
        run_id = request.data.get('run_id')
        run = get_object_or_404(TaskRun, pk=run_id, etl_task_id=task_id)
        run.state = TaskRunState.STOPPED
        run.save()
        return Response({'result': True}, status=status.HTTP_200_OK)
