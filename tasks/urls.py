from django.urls import path
from .views import (
    TaskListView, TaskCreateView, TaskUpdateView, TaskDeleteView, TaskToggleStatusView,
    AccountManageListView, AccountCreateView, AccountUpdateView, AccountDeleteView
)

urlpatterns = [
    # Quản lý Công việc
    path('', TaskListView.as_view(), name='dashboard'), # Trang chủ/Dashboard
    path('tasks/add/', TaskCreateView.as_view(), name='task_add'),
    path('tasks/<int:pk>/edit/', TaskUpdateView.as_view(), name='task_edit'),
    path('tasks/<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
    # View để cập nhật trạng thái (POST request cho checkbox)
    path('tasks/<int:pk>/toggle/<str:status_field>/', TaskToggleStatusView.as_view(), name='task_toggle_status'), 

    # Quản lý Tài khoản (Admin Only)
    path('accounts/manage/', AccountManageListView.as_view(), name='account_manage'),
    path('accounts/add/', AccountCreateView.as_view(), name='account_add'),
    path('accounts/<int:pk>/edit/', AccountUpdateView.as_view(), name='account_edit'),
    path('accounts/<int:pk>/delete/', AccountDeleteView.as_view(), name='account_delete'),
]