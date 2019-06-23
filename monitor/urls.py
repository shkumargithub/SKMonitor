from django.urls import path
from . import views

app_name = 'monitor'

urlpatterns = [
    # path('', views.index, name='index')
    path('', views.machine, name='machine'),
    path('<int:sno>/', views.machinedetails, name='machinedetails'),
    path('dashboard/', views.dashboard, name='dashboard')
]