from django.urls import path, re_path
from . import views

# namespace
app_name = 'myQ'

urlpatterns = [
    path('index/', views.index, name = 'index'),
    path('confirm_set_door/', views.confirm_set_door, name='send_email'),
    path('check_door_status/', views.check_door_status, name='check_door_status'),
    # path('set_door_status/', views.set_door_status, name='set_door_status'),
]