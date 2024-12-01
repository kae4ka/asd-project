from django.urls import path
from .views import (
    CreateUserView,
    GetUserView,
    AddRoleView,
    RemoveRoleView,
    AddAccessView,
    RemoveAccessView,
    ApproveAccessRequestView,
)

urlpatterns = [
    path('create_user/', CreateUserView.as_view(), name='create_user'),
    path('get_user/<str:user_id>/', GetUserView.as_view(), name='get_user'),
    path('add_role/', AddRoleView.as_view(), name='add_role'),
    path('remove_role/', RemoveRoleView.as_view(), name='remove_role'),
    path('add_access/', AddAccessView.as_view(), name='add_access'),
    path('remove_access/', RemoveAccessView.as_view(), name='remove_access'),
    path('approve_access_request/', ApproveAccessRequestView.as_view(), name='approve_access_request'),
]
