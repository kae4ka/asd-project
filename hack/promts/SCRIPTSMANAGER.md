# SCRIPTS MANAGER

## Prompt

- [ServiceName]: Scripts Manager
- [Description]: Сервис для создание и редактирования скриптов
- [Language]: язык Python
- [Framework]: фрейморк Django
- [Features]: 1. Создание и редактирование скриптов
- [ProtoContract]: syntax = "proto3";package etl.script.manager.V1;import "google/protobuf/wrappers.proto";service ScriptManager {    rpc CreateScript(CreateScriptRequest) returns (CreateScriptResponse);    rpc UpdateScript(UpdateScriptRequest) returns (UpdateScriptResponse);    rpc ReleaseScript(ReleaseScriptRequest) returns (ReleaseScriptResponse);    rpc GetScript(GetScriptRequest) returns (GetScriptResponse);    rpc GetAllScript(GetAllScriptRequest) returns (GetAllScriptResponse);}message CreateScriptRequest {    Script script = 1;}message CreateScriptResponse {    bool result = 1;}message UpdateScriptRequest {    string script_id = 1;    oneof script {        google.protobuf.Empty extractor = 2;        FieldRule field_rule = 3;        AnonymizationRule anonymization_rule = 4;        TransformationScript transformer = 5;        google.protobuf.Empty uploader = 6;    }    repeated Field fields_to_add = 7;    repeated Field fields_to_remove = 8;}message UpdateScriptResponse {    bool result = 1;}message ReleaseScriptRequest {    string script_id = 1;}message ReleaseScriptResponse {    bool result = 1;}message GetScriptRequest {    string script_id = 1;}message GetScriptResponse {    Script script = 1;}message GetAllScriptRequest {    string etl_task_id = 1;}message GetAllScriptResponse {    repeated Script scripts = 1;}message Script {    string id = 1;    string task_id = 2;    repeated Field fields = 3;    bool released = 4;    oneof script {        google.protobuf.Empty extractor = 5;        FieldRule field_rule = 6;        AnonymizationRule anonymization_rule = 7;        TransformationScript transformer = 8;        google.protobuf.Empty uploader = 9;    }}message FieldRule {    string default_value = 1;    string min_value = 2;    string max_value = 3;    FieldType field_type = 4;    FieldRuleType type = 5;}enum FieldType {    Integer = 0;    String = 1;    Double = 2;}enum FieldRuleType {    FillEmpty = 0;    IgnoreEmpty = 1;    RemoveEmpty = 2;    FillOutOfRange = 3;    IgnoreOutOfRange = 4;    RemoveOutOfRange = 5;}message AnonymizationRule {    AnonymizationRuleType type = 1;}enum AnonymizationRuleType {    Generalization = 0;    Suppression = 1;    Anatomization = 2;    Permutation = 3;    Pertubation = 3;}message TransformationScript {    google.protobuf.StringValue transformation_script = 1;    TransformationType type = 2;}enum TransformationType {    Merge = 0;    Update = 1;}message Field {    string ext_datamodule_id = 1;    string field_name = 2;}


Давай продолжим создание ETL-системы. Давай приступим к написанию нашего проекта и начнем с сервиса {SERVICENAME} в целом его можно охарактеризовать следующим образом: {Description}. Необходимо реализовать данный микросервис с использованием {LANGUAGE} и {FRAMEWORK}. Сервис должен реализовывать подготовленный прото-контрак: {PROTOCONTRACT}. Вот описание каждого метода:

Пока что мне необходимо сделать простую, но рабочую версию сервиса, который будет деплоиться в созданный K8s, поэтому 


Составь очень подробный параметризированный промт для создания сервисов


Создай полноценный сервис {ServiceName} для описанной ETL-системы со следующими требованиями:

1. Описание: {Description}
2. Функциональный возможности:
	- Сервис имеет следующий список функциональных возможностей: {Features}
3. Технологический стек:
	- Язык программирования: {Language}
	- Фреймворк: {Framework}
4. Развертывание:
	- Контейнеризация с помощью Docker
	- Развертывание в K8s
5. Требования к реализации:
	- Необходимо полностью описать создание сервиса по шагам от создания папки проекта до полной реализации
	- Необходимо реализовать полноценный сервис, с полностью описанными методами
	- Необходимо реализовать фичи ({Features}) используя обычный rest подход, но для реализации контрактов ориентируйся на прото-контракт: ({ProtoContract}). Все должно быть реализовано полностью
	- Должны быть созданы и полностью написаны необходимые файлы для запуска, развертывания и полной работоспособности проекта
	- В методы должен передаваться еще user_id и сервис должен ходить в user manager сервис, чтобы проверить доступ к редактированию
	- Добавь Swagger cподробным описанием каждого метода


Доступ к user manager
curl -X 'GET' \
  'http://84.201.148.234:8000/api/get_user/123/' \
  -H 'accept: application/json' \
  -H 'X-CSRFTOKEN: sKQnktsZJiKkwEuDfUGIb3XNGi2kXUwmwUQANkmmA5j0anY2puUVwOQ1CFIWTxo4'

{
  "id": "123",
  "name": "artem",
  "roles": [
    {
      "role": 1
    }
  ],
  "ext_datamodule_accesses": [
    {
      "id": 1,
      "ext_datamodule_id": "156",
      "access_types": [
        {
          "access_type": 1
        }
      ],
      "approved": true
    }
  ]
}

## Result

Понял, вы хотите избежать передачи `user_id` в каждом запросе и использовать более безопасный и стандартный подход к аутентификации пользователей. Вместо передачи `user_id` вручную, мы можем использовать **Token-Based Authentication** (например, **JWT**) для аутентификации пользователей. Это позволит автоматически получать информацию о пользователе из токена, предоставленного в заголовке запроса, и использовать её для проверки доступа.

Ниже приведены шаги по обновлению сервиса **Scripts Manager** для использования JWT аутентификации вместо передачи `user_id` в каждом запросе.

## Оглавление

1. [Установка необходимых пакетов](#1-установка-необходимых-пакетов)
2. [Настройка Django для использования JWT](#2-настройка-django-для-использования-jwt)
3. [Обновление моделей и сериализаторов](#3-обновление-моделей-и-сериализаторов)
4. [Обновление представлений (Views)](#4-обновление-представлений-views)
5. [Обновление маршрутов (URLs)](#5-обновление-маршрутов-urls)
6. [Добавление Swagger аутентификации](#6-добавление-swagger-аутентификации)
7. [Обновление Docker и Kubernetes конфигураций](#7-обновление-docker-и-kubernetes-конфигураций)
8. [Запуск и проверка обновленного сервиса](#8-запуск-и-проверка-обновленного-сервиса)
9. [Заключение](#9-заключение)

---

## 1. Установка необходимых пакетов

Для реализации JWT аутентификации нам потребуется установить пакет `djangorestframework-simplejwt`.

```bash
pip install djangorestframework-simplejwt
```

## 2. Настройка Django для использования JWT

Обновим настройки проекта для интеграции JWT аутентификации.

**scripts_manager/settings.py**

```python
# Добавьте Simple JWT в INSTALLED_APPS, если требуется
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'drf_yasg',
    'scripts',
]

# Настройка REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# Настройка Simple JWT (опционально)
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

## 3. Обновление моделей и сериализаторов

Поскольку мы уже используем кастомную модель пользователя, убедимся, что она правильно настроена.

**users/models.py**

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class UserRole(models.TextChoices):
    EDIT_TASK = 'EDIT_TASK', 'Edit Task'
    MANAGE_DATA = 'MANAGE_DATA', 'Manage Data'
    CREATE_EXT_DATAMODULE = 'CREATE_EXT_DATAMODULE', 'Create External Datamodule'
    PROCESS_ETL_TASK = 'PROCESS_ETL_TASK', 'Process ETL Task'

class ExtDatamoduleAccessType(models.TextChoices):
    READ = 'READ', 'Read'
    WRITE = 'WRITE', 'Write'
    OWNER = 'OWNER', 'Owner'

class User(AbstractUser):
    roles = models.CharField(max_length=255, choices=UserRole.choices, blank=True)

class ExtDatamodule(models.Model):
    name = models.CharField(max_length=255)
    # Дополнительные поля для описания внешнего датамодуля

class ExtDatamoduleAccess(models.Model):
    user = models.ForeignKey(User, related_name='ext_accesses', on_delete=models.CASCADE)
    ext_datamodule = models.ForeignKey(ExtDatamodule, on_delete=models.CASCADE)
    access_type = models.CharField(max_length=50, choices=ExtDatamoduleAccessType.choices)
    approved = models.BooleanField(default=False)
```

**users/serializers.py**

Добавим сериализатор для токенов JWT.

```python
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    ext_accesses = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'roles', 'ext_accesses']
```

**Создайте файл `users/urls.py` для аутентификации:**

```python
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

**Обновите основной файл маршрутов:**

**scripts_manager/urls.py**

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Scripts Manager API",
      default_version='v1',
      description="API документация для Scripts Manager",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@etl.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),  # Добавлено для аутентификации
    path('api/', include('scripts.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

## 4. Обновление представлений (Views)

Теперь обновим `ScriptManagerViewSet` для использования `request.user` вместо передачи `user_id`.

**scripts/views.py**

```python
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Script
from .serializers import ScriptSerializer
from django.shortcuts import get_object_or_404
import requests
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.permissions import IsAuthenticated

class ScriptManagerViewSet(viewsets.ViewSet):
    """
    ViewSet для управления скриптами.
    """

    USER_MANAGER_URL = 'http://user-manager-service/api/get_user/{user_id}/'  # Используйте внутренний сервисный URL

    def check_user_access(self, user):
        """
        Проверяет доступ пользователя через User Manager.
        """
        try:
            response = requests.get(
                self.USER_MANAGER_URL.format(user_id=user.id),
                headers={
                    'accept': 'application/json',
                    # Удалите CSRF токен, так как используем JWT
                },
                timeout=5
            )
            if response.status_code == 200:
                user_data = response.json()
                # Здесь можно добавить логику проверки ролей пользователя
                return True
            else:
                return False
        except requests.RequestException:
            return False

    @swagger_auto_schema(
        operation_description="Создание нового скрипта.",
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
        user = request.user
        if not self.check_user_access(user):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = ScriptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Обновление существующего скрипта.",
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
        - Поля, которые необходимо обновить (например, `content`, `fields`, `field_rule` и т.д.).

        **Пример тела запроса:**
        ```json
        {
            "content": "SELECT id, name FROM table;",
            "released": true
        }
        ```
        """
        user = request.user
        if not self.check_user_access(user):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        script = get_object_or_404(Script, pk=pk)
        serializer = ScriptSerializer(script, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': True}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Релиз скрипта (установка флага `released`).",
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
    )
    @action(detail=True, methods=['post'], url_path='release_script')
    def release_script(self, request, pk=None):
        """
        Релиз скрипта (установка флага `released`).

        **Параметры запроса:**
        - Отсутствуют, так как пользователь идентифицируется через JWT.

        **Пример тела запроса:**
        ```json
        {}
        ```
        """
        user = request.user
        if not self.check_user_access(user):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        script = get_object_or_404(Script, pk=pk)
        script.released = True
        script.save()
        return Response({'result': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Получение информации о скрипте по ID.",
        responses={
            200: openapi.Response(
                description="Информация о скрипте.",
                schema=ScriptSerializer
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
    @action(detail=True, methods=['get'], url_path='get_script')
    def get_script(self, request, pk=None):
        """
        Получение информации о скрипте по ID.

        **Параметры запроса:**
        - Отсутствуют, так как пользователь идентифицируется через JWT.

        **Пример запроса:**
        ```
        GET /api/scripts/1/get_script/
        ```
        """
        user = request.user
        if not self.check_user_access(user):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        script = get_object_or_404(Script, pk=pk)
        serializer = ScriptSerializer(script)
        return Response({'script': serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Получение всех скриптов для определенного ETL-задания.",
        manual_parameters=[
            openapi.Parameter(
                'etl_task_id',
                openapi.IN_QUERY,
                description="ID ETL-задания, для которого необходимо получить скрипты.",
                type=openapi.TYPE_STRING
            )
        ],
        responses={
            200: openapi.Response(
                description="Список скриптов для указанного ETL-задания.",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'scripts': ScriptSerializer(many=True)
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
    @action(detail=False, methods=['get'], url_path='get_all_scripts')
    def get_all_scripts(self, request):
        """
        Получение всех скриптов для определенного ETL-задания.

        **Параметры запроса:**
        - `etl_task_id` (string): ID ETL-задания, для которого необходимо получить скрипты.

        **Пример запроса:**
        ```
        GET /api/scripts/get_all_scripts/?etl_task_id=etl_task_1
        ```
        """
        user = request.user
        etl_task_id = request.query_params.get('etl_task_id')
        if not self.check_user_access(user):
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        scripts = Script.objects.filter(task_id=etl_task_id)
        serializer = ScriptSerializer(scripts, many=True)
        return Response({'scripts': serializer.data}, status=status.HTTP_200_OK)
```

**Пояснения:**

1. **Аутентификация через JWT:**
   - Удалены все передачи `user_id` в теле запроса или параметрах.
   - Используется `request.user` для получения текущего аутентифицированного пользователя.
   - Убедитесь, что клиент отправляет JWT токен в заголовке `Authorization: Bearer <token>`.

2. **Проверка доступа:**
   - Метод `check_user_access` теперь принимает объект пользователя и делает запрос к **User Manager** для проверки доступа.
   - Обновите `USER_MANAGER
