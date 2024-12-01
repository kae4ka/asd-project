from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Script
from .serializers import ScriptSerializer
from django.shortcuts import get_object_or_404
import requests
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ScriptManagerViewSet(viewsets.ViewSet):
    """
    ViewSet для управления скриптами.
    """

    USER_MANAGER_URL = 'http://84.201.148.234:8000/api/get_user/{user_id}/'

    def check_user_access(self, user_id):
        """
        Проверяет доступ пользователя через User Manager.
        """
        try:
            response = requests.get(
                self.USER_MANAGER_URL.format(user_id=user_id),
                headers={
                    'accept': 'application/json',
                    'X-CSRFTOKEN': 'sKQnktsZJiKkwEuDfUGIb3XNGi2kXUwmwUQANkmmA5j0anY2puUVwOQ1CFIWTxo4'
                },
                timeout=5
            )
            print(response)
            print(response.json())
            if response.status_code == 200:
                user_data = response.json()
                # Здесь можно добавить логику проверки ролей пользователя
                return True
            else:
                return False
        except requests.RequestException:
            return False

    def get_user_id_from_headers(self, request):
        """
        Извлекает user_id из заголовков запроса.
        """
        return request.headers.get('X-USER-ID')

    @swagger_auto_schema(
        operation_description="Создание нового скрипта.",
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя, запрашивающего скрипты.",
                type=openapi.TYPE_STRING
            ),
        ],
        request_body=ScriptSerializer,
        responses={
            201: openapi.Response(
                description="Скрипт успешно создан.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'result': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True)
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка валидации данных.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, example="Invalid data")
                    }
                )
            ),
            401: openapi.Response(
                description="Неавторизованный доступ.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, example="Unauthorized")
                    }
                )
            )
        }
    )
    @action(detail=False, methods=['post'], url_path='create_script')
    def create_script(self, request):
        """
        Создание нового скрипта.

        **Параметры запроса:**
        - `user_id` (string): ID пользователя, создающего скрипт.
        - `task_id` (string): ID ETL-задания, к которому относится скрипт.
        - `script_type` (string): Тип скрипта (extractor, field_rule, anonymization_rule, transformer, uploader).
        - `content` (string): Содержимое скрипта.
        - `fields` (array, optional): Список полей, связанных со скриптом.
        - `field_rule` (object, optional): Правила полей.
        - `anonymization_rule` (object, optional): Правила анонимизации.
        - `transformation_script` (object, optional): Скрипт трансформации.

        **Пример тела запроса:**
        ```json
        {
            "user_id": "123",
            "task_id": "etl_task_1",
            "script_type": "extractor",
            "content": "SELECT * FROM table;",
            "fields": [
                {
                    "ext_datamodule_id": "156",
                    "field_name": "column1"
                }
            ],
            "field_rule": {
                "default_value": "N/A",
                "min_value": "0",
                "max_value": "100",
                "field_type": "Integer",
                "type": "FillEmpty"
            }
        }
        ```
        """
        user_id = self.get_user_id_from_headers(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ScriptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Обновление существующего скрипта.",
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя, запрашивающего скрипты.",
                type=openapi.TYPE_STRING
            ),
        ],
        request_body=ScriptSerializer,
        responses={
            200: openapi.Response(
                description="Скрипт успешно обновлен.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'result': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True)
                    }
                )
            ),
            400: openapi.Response(
                description="Ошибка валидации данных.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, example="Invalid data")
                    }
                )
            ),
            401: openapi.Response(
                description="Неавторизованный доступ.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, example="Unauthorized")
                    }
                )
            ),
            404: openapi.Response(
                description="Скрипт не найден.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, example="Not found.")
                    }
                )
            )
        }
    )
    @action(detail=True, methods=['post'], url_path='update_script')
    def update_script(self, request, pk=None):
        """
        Обновление существующего скрипта.

        **Параметры запроса:**
        - `user_id` (string): ID пользователя, обновляющего скрипт.
        - Поля, которые необходимо обновить (например, `content`, `fields`, `field_rule` и т.д.).

        **Пример тела запроса:**
        ```json
        {
            "user_id": "123",
            "content": "SELECT id, name FROM table;",
            "released": true
        }
        ```
        """
        user_id = self.get_user_id_from_headers(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        script = get_object_or_404(Script, pk=pk)
        serializer = ScriptSerializer(script, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Релиз скрипта (установка флага `released`).",
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя, запрашивающего скрипты.",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: openapi.Response(
                description="Скрипт успешно релизнут.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'result': openapi.Schema(type=openapi.TYPE_BOOLEAN, example=True)
                    }
                )
            ),
            401: openapi.Response(
                description="Неавторизованный доступ.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, example="Unauthorized")
                    }
                )
            ),
            404: openapi.Response(
                description="Скрипт не найден.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, example="Not found.")
                    }
                )
            )
        }
    )
    @action(detail=True, methods=['post'], url_path='release_script')
    def release_script(self, request, pk=None):
        """
        Релиз скрипта (установка флага `released`).

        **Параметры запроса:**
        - `user_id` (string): ID пользователя, релизящего скрипт.

        **Пример тела запроса:**
        ```json
        {
            "user_id": "123"
        }
        ```
        """
        user_id = self.get_user_id_from_headers(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        script = get_object_or_404(Script, pk=pk)
        script.released = True
        script.save()
        return Response({'result': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Получение информации о скрипте по ID.",
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя, запрашивающего скрипты.",
                type=openapi.TYPE_STRING
            ),
        ],
        responses={
            200: ScriptSerializer(),
            401: openapi.Response(
                description="Неавторизованный доступ.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, example="Unauthorized")
                    }
                )
            ),
            404: openapi.Response(
                description="Скрипт не найден.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'detail': openapi.Schema(type=openapi.TYPE_STRING, example="Not found.")
                    }
                )
            )
        }
    )
    @action(detail=True, methods=['get'], url_path='get_script')
    def get_script(self, request, pk=None):
        """
        Получение информации о скрипте по ID.

        **Параметры запроса:**
        - `user_id` (string): ID пользователя, запрашивающего скрипт.

        **Пример запроса:**
        ```
        GET /api/scripts/1/get_script/?user_id=123
        ```
        """
        user_id = self.get_user_id_from_headers(request)
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        script = get_object_or_404(Script, pk=pk)
        serializer = ScriptSerializer(script)
        return Response({'script': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Получение всех скриптов для определенного ETL-задания.",
        manual_parameters=[
            openapi.Parameter(
                'X-USER-ID',
                openapi.IN_HEADER,
                description="ID пользователя, запрашивающего скрипты.",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'etl_task_id',
                openapi.IN_QUERY,
                description="ID ETL-задания, для которого необходимо получить скрипты.",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: ScriptSerializer(),
            401: openapi.Response(
                description="Неавторизованный доступ.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'error': openapi.Schema(type=openapi.TYPE_STRING, example="Unauthorized")
                    }
                )
            )
        }
    )
    @action(detail=False, methods=['get'], url_path='get_all_scripts')
    def get_all_scripts(self, request):
        """
        Получение всех скриптов для определенного ETL-задания.

        **Параметры запроса:**
        - `user_id` (string): ID пользователя, запрашивающего скрипты.

        **Пример запроса:**
        ```
        GET /api/scripts/get_all_scripts/?user_id=123&etl_task_id=etl_task_1
        ```
        """
        user_id = self.get_user_id_from_headers(request)
        etl_task_id = request.query_params.get('etl_task_id')
        if not self.check_user_access(user_id):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        scripts = Script.objects.filter(task_id=etl_task_id)
        serializer = ScriptSerializer(scripts, many=True)
        return Response({'scripts': serializer.data}, status=status.HTTP_200_OK)
