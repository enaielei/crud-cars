from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('update/<int:id>/', views.update, name="update"),
    path('delete/<int:id>/', views.delete, name="delete"),
    path('move_up/<int:id>/', views.move_up, name="move_up"),
    path('move_down/<int:id>/', views.move_down, name="move_down"),
]