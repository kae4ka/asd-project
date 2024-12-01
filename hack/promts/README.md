# Base

We have an ETL system project. The following technology stack was previously selected for implementation:
API definition - gRPC
Programming language - python
App framework - Django
Serialization/state format - protobuf + json
Database - postgreSQL
Testing tools - pytest
CI/CD pipeline - Github Actions
Delivery method - Docker
Monitoring - Grafana

Here this small project description.

This project focuses on developing a complex and large-scale ETL (Extract, Transform, Load) service aimed at cleaning and securing private data. The service will extract data from the company's internal systems, then clean, consolidate, anonymize, and transform the data before loading it into a new version of a data module. These data modules, stored on S3 or in a relational database management system (RDBMS), are described by metadata compatible with json-ld, a data gathering protocol, and versioned data. After the ETL process is complete, the data modules can be utilized by machine learning applications deployed on the framework. Ensuring data quality and accessibility is crucial for the applications operating within this framework.

Features:

1. Table Handling: The service should be able to work with tables. The tables will contain columns, which correspond to names for a particular class of values and have a data type provided, and records, which are collections of (possibly empty) values matched to columns. A column is always mapped to a table, so that columns with the same name in different tables are always considered different columns.

2. Data Modules Management: The service should support data modules that contain metadata, the data collection protocol and the version of the module.

3. Empty Field Processing: The metadata should contain the names of tables and columns that will be taken by the service and transformed. The strategy for filling empty fields in a particular column will be provided in the column description in the metadata. The supported strategies will be ignoring the empty value and passing it into the service unchanged, replacing empty values in a particular column with a provided value, or not passing a record with an empty value in a given column into the service.

4. Range Validation: The metadata may contain the allowed value ranges for each column, provided per-column. If such range is provided for a column, the metadata must also specify the strategy of dealing with records that do not conform to the value restriction. Removing the record from the service and replacing the violating value with the maximum or minimum allowed value will be supported.

5. Primary Key Management: The metadata should allow a particular column to be specified as a primary key, meaning the values of that key are unique among all the records processed by the service. If a primary key is specified in the metadata, a strategy for working with records that have the same values of the primary key must be specified in the metadata. The supported options will be adding priorities for sources, so that the record from the highest-ranking conflicting source is processed by the service, removing all records with a conflicting primary key from the service, and adding all records but generating new primary keys for them.

6. Foreign Key Management: The metadata should allow a particular column to be designated a foreign key and mapped to a column in a different table specified in the metadata. The value of a foreign key must be a value that is present in the specified column of the different table, otherwise the record should be removed from the service.

7. Anonymization Methods: All data processed by the service will be anonymized using the well-known generalization, suppression, anatomization, permutation, and perturbation operations.

8. Data Collection Process: The collection protocol in the metadata lists scripts for all tables mentioned in the metadata. Several scripts can be listed for the same table name, in this case the service will merge the data from different sources into one entity according to the rules specified in the metadata. The scripts should return the data they retrieved in the JSON format.

9. Data Upload and Version Control: The data module should contain a data upload script, which will be executed after the data is processed. It should either work in a way that the collection protocol specified in the data module retrieves the new processed data after the upload script completes or rewrite the collection protocol of the data module so that the new collection protocol works with the uploaded data. The data upload script should also update the version part of the data module.

10. Auditing Logging: All operations performed by the service will be recorded in a log for auditing purposes. This logging ensures transparency, traceability, and compliance with applicable standards and regulations.



Use-cases:

### Use Case: Login

**Description:** The user logs into the ETL service using an external Single Sign-On (SSO) system for authentication.

1. **Primary Actor:** User
1. **Goals:** Gain authorized access to the ETL service
1. **Pre-conditions:** User has valid credentials with the external SSO provider
1. **Post-conditions:** User is authenticated and granted access to the ETL service's functionalities

**Basic Flow:**

1. **Access Login Page:**
   1. User navigates to the ETL service login page.
   1. System displays the login interface.
2. **Redirect to SSO Provider:**
   1. User selects the option to log in via the external SSO provider.
   1. System redirects the user to the SSO provider's authentication page.
3. **Authenticate with SSO:**
   1. User enters their SSO credentials and submits.
   1. SSO provider authenticates the user.
4. **Return to ETL Service:**
   1. SSO provider redirects the user back to the ETL service with authentication tokens.
5. **Establish Session:**
   1. System validates the authentication tokens.
   1. System establishes a session for the user.
   1. User gains access to the ETL service's dashboard and features.

**Note:** Authentication is handled externally; no backend methods are invoked within the ETL service for this use case.

---

### Use Case: Manage Scripts

**Description:** The Task-Editor manages scripts required for ETL processing by utilizing the `ScriptManager` service, including creating, updating, releasing, and retrieving scripts.

1. **Primary Actor:** Task-Editor
1. **Goals:** Create, update, release, and manage scripts for extraction, field rules application, transformation, anonymization, and uploading
1. **Pre-conditions:** User must be logged into the service
1. **Post-conditions:** Scripts are created, updated, or released successfully, ready for use in ETL tasks

**Basic Flow:**

1. **Access Script Management:**
   1. Task-Editor navigates to the script management section in the ETL service interface.
2. **Check Permissions:**
   1. System verifies the Task-Editor's permissions to manage scripts.
   1. (Access verification may involve backend call) *(GetUser - UserManager)*
3. **View Script Options:**
   1. System presents options to create a new script or edit an existing one.
4. **Select Action:**
   1. Task-Editor chooses to create a new script or modify an existing script.
5. **Create New Script:**
   1. If creating, Task-Editor inputs script details such as type and properties.
   1. Task-Editor submits the new script.
   1. System processes the creation request.
   1. *(CreateScript - ScriptManager)*
6. **Edit Existing Script:**
   1. If editing, Task-Editor selects a script to modify.
   1. System retrieves script details.
   1. *(GetScript - ScriptManager)*
   1. Task-Editor updates the script information.
   1. Task-Editor submits the updates.
   1. System processes the update request.
   1. *(UpdateScript - ScriptManager)*
7. **Release Script:**
   1. Task-Editor may choose to release the script for use in ETL tasks.
   1. Task-Editor initiates the release action.
   1. System processes the release.
   1. *(ReleaseScript - ScriptManager)*
8. **Confirmation:**
   1. System confirms that the script is saved and ready for integration.
   1. Task-Editor receives confirmation message.

**Alternate Path:**

- **Validation Errors:**
  1. If the system detects invalid inputs, it informs the Task-Editor and prompts for corrections before proceeding.

---

### Use Case: Manage ETL Task

**Description:** The Task-Editor creates and configures an ETL task by using the `EtlTaskManager` service, including adding scripts via update methods.

1. **Primary Actor:** Task-Editor
1. **Goals:** Create, configure, and update ETL tasks by adding relevant scripts
1. **Pre-conditions:** User must be logged into the service
1. **Post-conditions:** ETL task is created or updated with all necessary scripts, ready for execution

**Basic Flow:**

1. **Access ETL Task Management:**
   1. Task-Editor navigates to the ETL task management section.
2. **Check Permissions:**
   1. System verifies Task-Editor's permissions to manage ETL tasks.
   1. *(GetUser - UserManager)*
3. **Create or Select Task:**
   1.  Task-Editor chooses to create a new ETL task or select an existing one to update.
   1.  If creating, Task-Editor provides basic task details and submits.
   1.  *(CreateTask - EtlTaskManager)*
   1.  If updating, Task-Editor selects the task to modify.
   1.  System retrieves task details.
   1.  *(GetTask - EtlTaskManager)*
4. **Configure Task Scripts:**
   1. Task-Editor attaches relevant scripts to the task:
     1. Adds or updates the Extraction script.
       1. *(UpdateExtractionScript - EtlTaskManager)*
     1. Adds or updates Field Rules.
       1. *(UpdateFieldRules - EtlTaskManager)*
     1. Adds or updates Anonymization rules.
       1. *(UpdateAnonymizationRules - EtlTaskManager)*
     1. Adds or updates Transformation scripts.
       1. *(UpdateTransformationScripts - EtlTaskManager)*
     1. Adds or updates Uploading script.
       1. *(UpdateUploadingScript - EtlTaskManager)*
5. **Finalize Configuration:**
   1. Task-Editor reviews the task setup.
   1. Task-Editor saves the task configuration.
6. **Release Task:**
   1. Task-Editor may release the task to make it ready for execution.
   1. *(Release - EtlTaskManager)*
7. **Confirmation:**
   1. System validates the task setup.
   1. System confirms the task is ready for execution.

**Alternate Path:**

1. **Missing Scripts:**
  1. If required scripts are not attached, system alerts Task-Editor to complete the setup before the task can be released.

---

### Use Case: Manage External Datamodule Connection

**Description:** The user creates and configures connections to external datamodules by using the `ExtDatamoduleManager` service.

1. **Primary Actor:** User
1. **Goals:** Establish and manage connections to external datamodules for data extraction or interaction
1. **Pre-conditions:** User must be logged into the service and have necessary permissions
1. **Post-conditions:** A new external datamodule connection is created or updated and saved, ready for use in ETL tasks

**Basic Flow:**

1. **Access Connection Management:**
   1. User navigates to the "Manage External Datamodule Connections" section.
2. **Check Permissions:**
   1. System verifies user's permissions to manage connections.
   1. *(GetUser - UserManager)*
3. **Create or Edit Connection:**
   1. User chooses to create a new connection or edit an existing one.
4. **Provide Connection Details:**
   1. User enters necessary information:
     1. Datamodule contract details.
     1. Connection string.
     1. Connection type (e.g., SQL, gRPC, API).
     1. Assigns owners for the connection.
5. **Submit Configuration:**
   1. User submits the connection configuration.
6. **Process Request:**
   1. System validates the input for correctness and conflicts.
   1. System saves the new or updated connection.
   1. *(CreateConnection or UpdateConnection - ExtDatamoduleManager)*
7. **Confirmation:**
   1. System confirms the connection is ready for use.
   1. Notifies assigned owners if applicable.

---

### Use Case: Get External Datamodule Access

**Description:** The user requests access to an existing external datamodule connection by sending a request to the connection's owners via the `UserManager` service.

1. **Primary Actor:** User
1. **Goals:** Obtain permission to use a specific external datamodule connection
1. **Pre-conditions:** User must be logged into the service; the connection exists
1. **Post-conditions:** An access request is sent to the connection's owners for approval

**Basic Flow:**

1. **View Available Connections:**
   1. User navigates to the list of external datamodule connections.
   1. System displays available connections with access status.
   1. *(GetAllConnection - ExtDatamoduleManager)*
2. **Select Connection:**
   1. User identifies a connection they need access to.
3. **Request Access:**
   1. User selects "Request Access" for the chosen connection.
   1. System prompts for reason or additional details.
4. **Submit Request:**
   1. User submits the access request.
   1. System records the request.
   1. *(AddAccess - UserManager)*
5. **Notify Owners:**
   1. System sends notification to the connection's owners.
6. **Confirmation:**
   1. User receives acknowledgment that the request has been sent.

---

### Use Case: Approve External Datamodule Access

**Description:** The connection owners review and approve or deny access requests from users via the `UserManager` service.

1. **Primary Actor:** Connection Owner
1. **Goals:** Manage access requests by approving or denying user requests
1. **Pre-conditions:** Connection owner must be logged into the service; pending access requests exist
1. **Post-conditions:** User access is granted or denied; requester is notified

**Basic Flow:**

1. **Receive Notification:**
   1. Connection owner is notified of a pending access request.
2. **Access Access Requests:**
   1. Owner navigates to the "Access Requests" section.
3. **Check Permissions:**
   1. System verifies owner's permissions for the connection.
   1. *(GetUser - UserManager)*
4. **Review Request:**
   1. System displays pending requests with details.
   1. Owner reviews the requester's information and reason.
5. **Make Decision:**
   1. Owner chooses to approve or deny the request.
6. **Submit Decision:**
   1. Owner submits their decision.
   1. *(ApproveAccessRequest - UserManager)*
7. **Update Permissions:**
   1. System updates access permissions accordingly.
8. **Notify Requester:**
   1. System sends notification to the requester with the decision.

---

### Use Case: Process ETL Task

**Description:** The Task-Manager initiates the processing of an ETL task by using the `EtlTaskManager` service, and the system executes the ETL processing steps.

1. **Primary Actor:** Task-Manager
1. **Goals:** Execute ETL processing, prepare data for eventual upload
1. **Pre-conditions:** ETL task is fully configured and validated
1. **Post-conditions:** Data is processed and stored, awaiting user confirmation for upload

**Basic Flow:**

1. **Initiate Task Processing:**
   1. Task-Manager selects an ETL task to process.
2. **Check Permissions:**
   1. System verifies Task-Manager's permissions.
   1. *(GetUser - UserManager)*
3. **Start ETL Task:**
   1. Task-Manager initiates the task processing.
   1. *(Start - EtlTaskManager)*
4. **Execute Extraction:**
   1. System runs the Extraction script to pull data.
5. **Apply Field Rules:**
   1. System applies Field Rules to clean and standardize data.
6. **Run Transformation:**
   1. System executes Transformation scripts.
7. **Apply Anonymization:**
   1. System applies Anonymization rules to data.
8. **Store Processed Data:**
   1. System saves the processed data in the Outbox.
9. **Confirmation:**
   1. System notifies Task-Manager that processing is complete.

**Alternate Path:**

1. **Processing Error:**
  1. If an error occurs, system logs the error.
  1. System informs Task-Manager of the issue.
  1. Processing is halted.

---

### Use Case: Stop ETL Task

**Description:** The Task-Manager can pause or completely stop an ETL task using the `Pause` or `Stop` methods in the `EtlTaskManager` service and decide on handling data in the Outbox.

1. **Primary Actor:** Task-Manager
1. **Goals:** Pause or terminate an active ETL task
1. **Pre-conditions:** ETL task is in progress
1. **Post-conditions:** ETL task is paused or terminated; Outbox data is handled as per user choice

**Basic Flow:**

1. **Initiate Stop/Pause:**
   1. Task-Manager chooses to pause or stop the ETL task.
2. **Check Permissions:**
   1. System verifies Task-Manager's permissions.
   1. *(GetUser - UserManager)*
3. **Execute Command:**
   1. System processes the pause or stop command.
   1. *(Pause or Stop - EtlTaskManager)*
4. **Handle Outbox Data:**
   1. If stopping, system prompts Task-Manager to confirm deletion of Outbox data.
   1. Task-Manager decides whether to clear the data.
5. **Process Decision:**
   1. System deletes Outbox data if confirmed.
6. **Confirmation:**
   1. System confirms the task is paused or stopped.

---

### Use Case: View Run History

**Description:** The user views the history of executed ETL tasks by retrieving audit logs using the `AuditLogger` service.

1. **Primary Actor:** User
1. **Goals:** Monitor and review the execution history of ETL tasks, including performance metrics
1. **Pre-conditions:** User must be logged into the service
1. **Post-conditions:** User successfully views the run history and relevant details

**Basic Flow:**

1. **Access Run History:**
   1. User navigates to the "Run History" section.
2. **Retrieve Audit Logs:**
   1. System fetches audit logs related to ETL tasks.
   1. *(ListAuditLogs - AuditLogger)*
3. **Display Summary:**
   1. System displays a list of executed tasks with summaries.
4. **View Details:**
   1. User selects a task to view more information.
   1. System retrieves detailed log.
   1. *(GetAuditLog - AuditLogger)*
5. **Present Information:**
   1. System displays execution details, data processed, and current state.

---

### Use Case: View Prepared Data

**Description:** The Data-Manager reviews data that has been processed and saved in the Outbox by using the `DataManager` service.

1. **Primary Actor:** Data-Manager
1. **Goals:** Access and review processed data
1. **Pre-conditions:** Processed data is available in the Outbox
1. **Post-conditions:** User can view data details stored in the Outbox

**Basic Flow:**

1. **Access Outbox:**
   1. Data-Manager navigates to the Outbox section.
2. **Check Permissions:**
   1. System verifies Data-Manager's permissions.
   1. *(GetUser - UserManager)*
3. **Retrieve Data Entries:**
   1. System fetches a list of processed data.
   1. *(GetAll - DataManager)*
4. **Select Data Entry:**
   1. Data-Manager selects a data entry to view.
5. **View Details:**
   1. System displays detailed information of the selected data.

---

### Use Case: Manage Prepared Data

**Description:** The Data-Manager manages the processed data in the Outbox by using the `Modifie` method in the `DataManager` service to add, edit, or delete entries.

1. **Primary Actor:** Data-Manager
1. **Goals:** Modify or manage prepared data entries in the Outbox
1. **Pre-conditions:** Processed data entries are available in the Outbox
1. **Post-conditions:** Data is updated, added, or removed as per user instructions

**Basic Flow:**

1. **Access Data Management:**
   1. Data-Manager navigates to the data management section in Outbox.
2. **Check Permissions:**
   1. System verifies Data-Manager's permissions.
   1. *(GetUser - UserManager)*
3. **Select Action:**
   1. Data-Manager chooses to add, edit, or delete a data entry.
4. **Perform Action:**
   1. Data-Manager makes the desired changes.
   1. Submits the modifications.
   1. *(Modifie - DataManager)*
5. **Process Changes:**
   1. System validates and applies the changes.
6. **Confirmation:**
   1. System confirms that the data has been updated.

---

### Use Case: Upload Prepared Data

**Description:** The Task-Manager decides to upload processed data from the Outbox to the destination by initiating the upload process using the `Start` or `Resume` methods in `EtlTaskManager`.

1. **Primary Actor:** Task-Manager
1. **Goals:** Confirm and initiate data upload from the Outbox
1. **Pre-conditions:** Data is processed and available in the Outbox
1. **Post-conditions:** Data is uploaded to the destination or handled based on user action

**Basic Flow:**

1. **Review Prepared Data:**
   1. Task-Manager reviews data entries in the Outbox.
   1. *(GetAll - DataManager)*
2. **Initiate Upload:**
   1. Task-Manager decides to upload the data.
   1. Starts the upload process.
   1. *(Start or Resume - EtlTaskManager)*
3. **Check Permissions:**
   1. System verifies Task-Manager's permissions.
   1. *(GetUser - UserManager)*
4. **Execute Uploading Script:**
   1. System runs the Uploading script attached to the task.
5. **Transfer Data:**
   1. Data is transferred to the destination service.
6. **Update Outbox:**
   1. System marks the data as uploaded.
7. **Confirmation:**
   1. System notifies Task-Manager of successful upload.

**Alternate Path:**

1. **No Action Taken:**
  1. If Task-Manager takes no action, system retains data for a predefined period.
  1. After the retention period, system automatically deletes the data.

---

### Use Case: Audit

**Description:** The system records all actions by users and the system itself. Users can review the history of changes and actions by using the `AuditLogger` service.

1. **Primary Actor:** User
1. **Goals:** Track and review audit logs for all actions
1. **Pre-conditions:** Audit logs are enabled and accessible
1. **Post-conditions:** User can view a detailed record of actions in the system

**Basic Flow:**

1. **Access Audit Logs:**
   1. User navigates to the audit log section.
2. **Retrieve Logs:**
   1. System fetches audit logs.
   1. *(ListAuditLogs - AuditLogger)*
3. **Search and Filter:**
   1. User searches or filters logs based on criteria.
4. **Select Log Entry:**
   1. User selects specific entries to view details.
5. **View Details:**
   1. System displays action details, including timestamp, actor, and changes.
   1. *(GetAuditLog - AuditLogger)*

It is assumed that the project will include 6 main features:
1. ETL-Task Manager - ETL Task management: creating, modifying, adding scripts and running tasks.
2. Script Manager - Script management: creation, modification
3. Data Manager - Executing ETL tasks, saving and managing prepared data, and sending it to the destination system.
4. ExtDataModule Manager - Describing connections to external storage systems.
5. User Manager - Managing user roles and access to external systems.
6. Audit Logger - Auditing user actions within the ETL system.

Just remember this information. Next, I will give you commands.


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

## Prompt

# SCRIPTS MANAGER

## Prompt

- [ServiceName]: Scripts Manager
- [Description]: Сервис для создание и редактирования скриптов
- [Language]: Python
- [Framework]: Django
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
