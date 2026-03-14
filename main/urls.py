from django.urls import path
from . import views

urlpatterns = [
    path('manage-questions/', views.manage_questions, name='manage_questions'),
    path('add-question/', views.add_question, name='add_question'),
    path('test/<int:category_id>/', views.take_test, name='take_test'),
    path('delete-question/<int:pk>/', views.delete_question, name='delete_question'),
    path('modules/', views.module_list, name='module_list'),
    path('presentations/', views.presentation_list, name='presentation_list'),
    path('categories/', views.category_list, name='category_list'),
    path('results/', views.test_results_list, name='test_results_list'),
]