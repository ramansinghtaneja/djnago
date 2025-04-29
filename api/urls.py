from django.urls import path
from . import views

urlpatterns = [
    
     path('interview', views.home, name='home'),
    path('test/', views.testt, name='testt'), 
    path('profiles/', views.profile_list, name='profile_list'),
    path('profiles/filters', views.profile_list_filter, name='profile_list'),
    path('profiles/summary', views.get_summery, name='filter_form'),
    path('shortlist/', views.profile_shortlist, name='shortlist'),
    # path('assessments/', views.assessment_details, name='assessment_details'),
    path('questions/', views.get_candidate_questions, name='assessment_details'),
    path('assessments/', views.assessment_details, name='assessment_details'),
    path('shortlist/', views.profile_shortlist, name='shortlist'),
]
