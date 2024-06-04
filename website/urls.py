from django.urls import path

from .views import home, logout_user, register_user, customer_record

urlpatterns = [
    path('', home, name='home'),
    path('logout/', logout_user, name='logout'),
    path('register/', register_user, name='register'),
    path('record/<int:pk>/', customer_record, name='record'),
]
