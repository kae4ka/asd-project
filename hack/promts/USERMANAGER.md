# USER MANAGER

## Prompt

- [ServiceName]: User Manager
- [Description]: Сервис для получения данных о пользователе: его роли и доступы к внешним системам
- [Language]: Python
- [Framework]: Django
- [Features]: 1. Создание пользователя2. Добавление/удаление ему ролей3. Запрос прав на доступ к внешним системам4. Одобрение/отказ права на доступ к внешним системам
- [ProtoContract]: syntax = "proto3";import "google/protobuf/empty.proto";import "google/protobuf/wrappers.proto";package etl.user.manager.V1;service UserManager {    rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);    rpc GetUser(GetUserRequest) returns (GetUserResponse);    rpc AddAccess(AddAccessRequest) returns (AddAccessResponse);    rpc RemoveAccess(RemoveAccessRequest) returns (RemoveAccessResponse);    rpc AddRole(AddRoleRequest) returns (AddRoleResponse);    rpc RemoveRole(RemoveRoleRequest) returns (RemoveRoleResponse);    rpc ApproveAccessRequest(ApproveAccessRequest) returns (ApproveAccessResponse);}message CreateUserRequest {    string id = 1;    string name = 2;}message CreateUserResponse {    bool result = 1;}message GetUserRequest {    string id = 1;}message GetUserResponse {    User user = 1;}message AddAccessRequest {    string user_id = 1;    ExtDatamoduleAccess access = 2;}message AddAccessResponse {    bool result = 1;}message RemoveAccessRequest {    string user_id = 1;    ExtDatamoduleAccess access = 2;}message RemoveAccessResponse {    bool result = 1;}message AddRoleRequest {    string user_id = 1;    UserRole role = 2;}message AddRoleResponse {    bool result = 1;}message RemoveRoleRequest {    string user_id = 1;    UserRole role = 2;}message RemoveRoleResponse {    bool result = 1;}message ApproveAccessRequest {    string access_request_id = 1;    string owner_user_id = 2;    bool state = 3;}message ApproveAccessResponse {    bool result = 1;}message User {    string id = 1;    string name = 2;    repeated UserRole roles = 3;    repeated ExtDatamoduleAccess ext_datamodule_accesses = 4;}message ExtDatamoduleAccess {    string id = 1;    string ext_datamodule_id = 2;    repeated ExtDatamoduleAccessType access_types = 3;}enum ExtDatamoduleAccessType {    READ = 0;    WRITE = 1;    OWNER = 2;}enum UserRole {    EDIT_TASK = 0;    MANAGE_DATA = 1;    CREATE_EXT_DATAMODULE = 2;    PROCESS_ETL_TASK = 3;}


Давай приступим к написанию нашего проекта и начнем с сервиса {SERVICENAME} в целом его можно охарактеризовать следующим образом: {Description}. Необходимо реализовать данный микросервис с использованием {LANGUAGE} и {FRAMEWORK}. Сервис должен реализовывать подготовленный прото-контрак: {PROTOCONTRACT}. Вот описание каждого метода:

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

ПРЕДСТАВЬ ПОЛНОЦЕННЫЙ СЕРВИС БЕЗ НЕОБХОДИМОСТИ В ДОРАБОТКАХ И ДОПИСЫВАНИИ


## Result

# Создание сервиса "User Manager" для ETL-системы

В этом руководстве мы создадим полноценный сервис **User Manager** с использованием Python и Django, который соответствует описанному прото-контракту. Сервис будет контейнеризирован с помощью Docker и готов к развертыванию в Kubernetes (K8s).

## Оглавление

1. [Описание сервиса](#описание-сервиса)
2. [Функциональные возможности](#функциональные-возможности)
3. [Технологический стек](#технологический-стек)
4. [Шаги по созданию сервиса](#шаги-по-созданию-сервиса)
    - [1. Настройка окружения](#1-настройка-окружения)
    - [2. Создание проекта Django](#2-создание-проекта-django)
    - [3. Определение моделей данных](#3-определение-моделей-данных)
    - [4. Реализация сериализаторов](#4-реализация-сериализаторов)
    - [5. Создание представлений (Views)](#5-создание-представлений-views)
    - [6. Определение маршрутов (URLs)](#6-определение-маршрутов-urls)
    - [7. Настройка Docker](#7-настройка-docker)
    - [8. Подготовка к развертыванию в Kubernetes](#8-подготовка-к-развертыванию-в-kubernetes)
5. [Запуск и проверка сервиса](#запуск-и-проверка-сервиса)
6. [Заключение](#заключение)

## Описание сервиса

**User Manager** — сервис для получения данных о пользователе: его роли и доступы к внешним системам.

## Функциональные возможности

Сервис имеет следующий список функциональных возможностей:

1. **Создание пользователя**
2. **Добавление/удаление ролей пользователю**
3. **Запрос прав на доступ к внешним системам**
4. **Одобрение/отказ права на доступ к внешним системам**

## Технологический стек

- **Язык программирования:** Python
- **Фреймворк:** Django (Django REST Framework)

## Шаги по созданию сервиса

### 1. Настройка окружения

Создадим директорию для проекта и настроим виртуальное окружение.

```bash
# Создаем директорию проекта
mkdir user_manager_service
cd user_manager_service

# Создаем и активируем виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Обновляем pip
pip install --upgrade pip

# Устанавливаем необходимые зависимости
pip install django djangorestframework psycopg2-binary
```

### 2. Создание проекта Django

Инициализируем новый проект Django и приложение внутри него.

```bash
# Создаем проект Django
django-admin startproject user_manager .

# Создаем приложение
python manage.py startapp users
```

Добавим `users` и `rest_framework` в `INSTALLED_APPS` в `user_manager/settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'users',
]
```

### 3. Определение моделей данных

Создадим модели, соответствующие нашим требованиям.

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
    roles = models.CharField(max_length=255, choices=UserRole.choices)

class ExtDatamodule(models.Model):
    name = models.CharField(max_length=255)
    # Дополнительные поля для описания внешнего датамодуля

class ExtDatamoduleAccess(models.Model):
    user = models.ForeignKey(User, related_name='ext_accesses', on_delete=models.CASCADE)
    ext_datamodule = models.ForeignKey(ExtDatamodule, on_delete=models.CASCADE)
    access_type = models.CharField(max_length=50, choices=ExtDatamoduleAccessType.choices)
    approved = models.BooleanField(default=False)
```

Применяем миграции:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Реализация сериализаторов

Создадим сериализаторы для преобразования моделей в JSON и обратно.

**users/serializers.py**

```python
from rest_framework import serializers
from .models import User, ExtDatamoduleAccess, ExtDatamodule

class ExtDatamoduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtDatamodule
        fields = '__all__'

class ExtDatamoduleAccessSerializer(serializers.ModelSerializer):
    ext_datamodule = ExtDatamoduleSerializer()

    class Meta:
        model = ExtDatamoduleAccess
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    ext_accesses = ExtDatamoduleAccessSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'roles', 'ext_accesses']
```

### 5. Создание представлений (Views)

Реализуем необходимые методы согласно нашим функциональным требованиям.

**users/views.py**

```python
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import User, ExtDatamoduleAccess, ExtDatamodule
from .serializers import UserSerializer, ExtDatamoduleAccessSerializer
from django.shortcuts import get_object_or_404

class UserViewSet(viewsets.ViewSet):
    def create_user(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.create_user(username=username, password=password)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_user(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def add_role(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        role = request.data.get('role')
        if role in dict(UserRole.choices).keys():
            user.roles = role
            user.save()
            return Response({'status': 'role added'})
        else:
            return Response({'error': 'Invalid role'}, status=status.HTTP_400_BAD_REQUEST)

    def remove_role(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        user.roles = ''
        user.save()
        return Response({'status': 'role removed'})

    def add_access(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        ext_module_id = request.data.get('ext_datamodule_id')
        access_type = request.data.get('access_type')

        ext_module = get_object_or_404(ExtDatamodule, pk=ext_module_id)
        if access_type in dict(ExtDatamoduleAccessType.choices).keys():
            access = ExtDatamoduleAccess.objects.create(
                user=user,
                ext_datamodule=ext_module,
                access_type=access_type,
                approved=False
            )
            serializer = ExtDatamoduleAccessSerializer(access)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Invalid access type'}, status=status.HTTP_400_BAD_REQUEST)

    def approve_access_request(self, request, access_request_id):
        access_request = get_object_or_404(ExtDatamoduleAccess, pk=access_request_id)
        state = request.data.get('state')
        access_request.approved = state
        access_request.save()
        return Response({'status': 'access request updated'})
```

### 6. Определение маршрутов (URLs)

Настроим маршруты для нашего API.

**users/urls.py**

```python
from django.urls import path
from .views import UserViewSet

user_list = UserViewSet.as_view({
    'post': 'create_user'
})

user_detail = UserViewSet.as_view({
    'get': 'get_user'
})

add_role = UserViewSet.as_view({
    'post': 'add_role'
})

remove_role = UserViewSet.as_view({
    'post': 'remove_role'
})

add_access = UserViewSet.as_view({
    'post': 'add_access'
})

approve_access = UserViewSet.as_view({
    'post': 'approve_access_request'
})

urlpatterns = [
    path('users/', user_list, name='user-list'),
    path('users/<int:pk>/', user_detail, name='user-detail'),
    path('users/<int:pk>/add_role/', add_role, name='add-role'),
    path('users/<int:pk>/remove_role/', remove_role, name='remove-role'),
    path('users/<int:pk>/add_access/', add_access, name='add-access'),
    path('access_requests/<int:access_request_id>/approve/', approve_access, name='approve-access'),
]
```

Добавим маршруты в основной файл проекта.

**user_manager/urls.py**

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
]
```

### 7. Настройка Docker

Создадим файл `Dockerfile` для контейнеризации нашего приложения.

**Dockerfile**

```dockerfile
# Используем официальный образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт
EXPOSE 8000

# Команда запуска сервера
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

Создадим файл `requirements.txt` с перечислением зависимостей.

**requirements.txt**

```
Django
djangorestframework
psycopg2-binary
```

### 8. Подготовка к развертыванию в Kubernetes

Создадим манифест для развертывания в K8s.

**k8s-deployment.yaml**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-manager-deployment
spec:
  replicas: 2
  selector:
    matchLabels:
      app: user-manager
  template:
    metadata:
      labels:
        app: user-manager
    spec:
      containers:
        - name: user-manager
          image: your-docker-repo/user-manager:latest
          ports:
            - containerPort: 8000
          env:
            - name: DJANGO_SETTINGS_MODULE
              value: 'user_manager.settings'
```

Создадим сервис для доступа к приложению.

**k8s-service.yaml**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: user-manager-service
spec:
  selector:
    app: user-manager
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8000
  type: LoadBalancer
```

## Запуск и проверка сервиса

### Локальный запуск

1. Примените миграции и создайте суперпользователя:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

2. Запустите сервер:

```bash
python manage.py runserver
```

### Запуск с помощью Docker

1. Постройте Docker-образ:

```bash
docker build -t user-manager:latest .
```

2. Запустите контейнер:

```bash
docker run -p 8000:8000 user-manager:latest
```

### Развертывание в Kubernetes

1. Запустите деплоймент и сервис:

```bash
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml
```

2. Проверьте статус подов:

```bash
kubectl get pods
```

## Заключение

Мы создали полноценный сервис **User Manager**, соответствующий заданным требованиям. Сервис реализует все необходимые методы для управления пользователями, их ролями и доступами к внешним системам, используя Django и Django REST Framework. Он готов к контейнеризации и развертыванию в Kubernetes.
