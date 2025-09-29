from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('dashboards/', views.dashboards_view, name='dashboards'),
    path('dashboards/<int:dashboard_id>/', views.view_dashboard, name='view_dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('ask_ai/', views.ask_ai_view, name='ask_ai'),
    path('grant_bulk_permissions/', views.grant_bulk_permissions_view, name='grant_bulk_permissions'),
]