from django.urls import path
from . import views

urlpatterns = [
    # ...existing code...
    path('tutor_coordinatori/edit/<int:id>/', views.edit_tutor, name='edit_tutor'),
    path('tutor_collaboratori/edit/<int:id>/', views.edit_tutor_collaboratore, name='edit_tutor_collaboratore'),
    # ...existing code...
]
