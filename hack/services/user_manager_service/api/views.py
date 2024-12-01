from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, ExtDatamoduleAccess, Role, AccessType
from .serializers import UserSerializer


class CreateUserView(APIView):
    @swagger_auto_schema(
        operation_description="Создание нового пользователя",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_STRING, description='ID пользователя'),
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='Имя пользователя'),
            },
            required=['id', 'name'],
        ),
        responses={
            200: openapi.Response(
                description="Результат создания",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'result': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Успех операции'),
                    },
                ),
            ),
            400: "Bad Request",
        },
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': True}, status=200)
        else:
            return Response({'result': False, 'errors': serializer.errors}, status=400)


class GetUserView(APIView):
    @swagger_auto_schema(
        operation_description="Получение данных о пользователе",
        responses={
            200: UserSerializer(),
            404: "User not found",
        },
    )
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=200)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)


class AddRoleView(APIView):
    @swagger_auto_schema(
        operation_description="Добавление роли пользователю",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='ID пользователя'),
                'role': openapi.Schema(type=openapi.TYPE_INTEGER,
                                       description='Роль пользователя (0: EDIT_TASK, 1: MANAGE_DATA, 2: CREATE_EXT_DATAMODULE, 3: PROCESS_ETL_TASK, 4: Unknown)'),
            },
            required=['user_id', 'role'],
        ),
        responses={
            200: openapi.Response(
                description="Результат добавления роли",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'result': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    },
                ),
            ),
            400: "Bad Request",
        },
    )
    def post(self, request):
        user_id = request.data.get('user_id')
        role_value = request.data.get('role')

        if user_id is None or role_value is None:
            return Response({'result': False, 'error': 'user_id and role are required'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            role, created = Role.objects.get_or_create(role=role_value)
            user.roles.add(role)
            return Response({'result': True}, status=200)
        except User.DoesNotExist:
            return Response({'result': False, 'error': 'User not found'}, status=404)


class RemoveRoleView(APIView):
    @swagger_auto_schema(
        operation_description="Удаление роли у пользователя",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='ID пользователя'),
                'role': openapi.Schema(type=openapi.TYPE_INTEGER, description='Роль пользователя'),
            },
            required=['user_id', 'role'],
        ),
        responses={
            200: openapi.Response(
                description="Результат удаления роли",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'result': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                    },
                ),
            ),
            400: "Bad Request",
        },
    )
    def post(self, request):
        user_id = request.data.get('user_id')
        role_value = request.data.get('role')

        if user_id is None or role_value is None:
            return Response({'result': False, 'error': 'user_id and role are required'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            role = Role.objects.get(role=role_value)
            user.roles.remove(role)
            return Response({'result': True}, status=200)
        except (User.DoesNotExist, Role.DoesNotExist):
            return Response({'result': False, 'error': 'User or Role not found'}, status=404)


class AddAccessView(APIView):
    @swagger_auto_schema(
        operation_description="Добавление доступа к внешней системе",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='ID пользователя'),
                'access': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ext_datamodule_id': openapi.Schema(type=openapi.TYPE_STRING,
                                                            description='ID внешнего модуля данных'),
                        'access_types': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_INTEGER),
                            description='Список типов доступа (0: READ, 1: WRITE, 2: OWNER)'
                        ),
                    },
                    required=['ext_datamodule_id', 'access_types'],
                ),
            },
            required=['user_id', 'access'],
        ),
        responses={
            200: openapi.Response(
                description="Результат добавления доступа",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'result': openapi.Schema(type=openapi.TYPE_BOOLEAN)},
                ),
            ),
            400: "Bad Request",
        },
    )
    def post(self, request):
        user_id = request.data.get('user_id')
        access_data = request.data.get('access')

        if user_id is None or access_data is None:
            return Response({'result': False, 'error': 'user_id and access are required'}, status=400)

        ext_datamodule_id = access_data.get('ext_datamodule_id')
        access_types_values = access_data.get('access_types')

        if ext_datamodule_id is None or access_types_values is None:
            return Response({'result': False, 'error': 'ext_datamodule_id and access_types are required'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            ext_access, created = ExtDatamoduleAccess.objects.get_or_create(ext_datamodule_id=ext_datamodule_id)
            for access_type_value in access_types_values:
                access_type, _ = AccessType.objects.get_or_create(access_type=access_type_value)
                ext_access.access_types.add(access_type)
            user.ext_datamodule_accesses.add(ext_access)
            return Response({'result': True}, status=200)
        except User.DoesNotExist:
            return Response({'result': False, 'error': 'User not found'}, status=404)


class RemoveAccessView(APIView):
    @swagger_auto_schema(
        operation_description="Удаление доступа к внешней системе",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='ID пользователя'),
                'access': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'ext_datamodule_id': openapi.Schema(type=openapi.TYPE_STRING,
                                                            description='ID внешнего модуля данных'),
                        'access_types': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Items(type=openapi.TYPE_INTEGER),
                            description='Список типов доступа'
                        ),
                    },
                    required=['ext_datamodule_id', 'access_types'],
                ),
            },
            required=['user_id', 'access'],
        ),
        responses={
            200: openapi.Response(
                description="Результат удаления доступа",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'result': openapi.Schema(type=openapi.TYPE_BOOLEAN)},
                ),
            ),
            400: "Bad Request",
        },
    )
    def post(self, request):
        user_id = request.data.get('user_id')
        access_data = request.data.get('access')

        if user_id is None or access_data is None:
            return Response({'result': False, 'error': 'user_id and access are required'}, status=400)

        ext_datamodule_id = access_data.get('ext_datamodule_id')
        access_types_values = access_data.get('access_types')

        if ext_datamodule_id is None or access_types_values is None:
            return Response({'result': False, 'error': 'ext_datamodule_id and access_types are required'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            ext_access = ExtDatamoduleAccess.objects.get(ext_datamodule_id=ext_datamodule_id)
            for access_type_value in access_types_values:
                access_type = AccessType.objects.get(access_type=access_type_value)
                ext_access.access_types.remove(access_type)
            if not ext_access.access_types.exists():
                user.ext_datamodule_accesses.remove(ext_access)
                ext_access.delete()
            return Response({'result': True}, status=200)
        except (User.DoesNotExist, ExtDatamoduleAccess.DoesNotExist, AccessType.DoesNotExist):
            return Response({'result': False, 'error': 'User or Access not found'}, status=404)


class ApproveAccessRequestView(APIView):
    @swagger_auto_schema(
        operation_description="Одобрение или отказ в запросе на доступ",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'ext_datamodule_id': openapi.Schema(type=openapi.TYPE_STRING, description='ID external datamodule'),
                'user_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='ID запрашиваемого'),
                'state': openapi.Schema(type=openapi.TYPE_BOOLEAN,
                                        description='Статус одобрения (True - одобрить, False - отказать)'),
            },
            required=['ext_datamodule_id', 'user_id', 'owner_user_id', 'state'],
        ),
        responses={
            200: openapi.Response(
                description="Результат обработки запроса",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={'result': openapi.Schema(type=openapi.TYPE_BOOLEAN)},
                ),
            ),
            400: "Bad Request",
        },
    )
    def post(self, request):
        ext_datamodule_id = request.data.get('ext_datamodule_id')
        user_id = request.data.get('user_id')
        state = request.data.get('state')

        if ext_datamodule_id is None or user_id is None is None or state is None:
            return Response({'result': False, 'error': 'All fields are required'}, status=400)

        try:
            user = User.objects.get(id=user_id)
            access = user.ext_datamodule_accesses.get(ext_datamodule_id=ext_datamodule_id)
            access.approved = state
            access.save()
            return Response({'result': True}, status=200)
        except (ExtDatamoduleAccess.DoesNotExist, User.DoesNotExist):
            return Response({'result': False, 'error': 'Access request or owner user not found'}, status=404)
