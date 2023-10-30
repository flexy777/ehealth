from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('user_records/', views.user_records_view, name='user_records'),
    path('logout/', views.logout_view, name='logout'),
    path('search_health_workers/', views.search_health_workers, name='search_health_workers'),
    path('book_appointment/<uuid:health_worker_id>/', views.book_appointment, name='book_appointment'),
    path('health_worker/dashboard/', views.health_worker_dashboard, name='health_worker_dashboard'),
    ]