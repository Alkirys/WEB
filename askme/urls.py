from django.http import HttpResponse, HttpRequest
from django.urls import path

from app import views


urlpatterns = [
    path('', views.all_questions, name = 'all_questions'),
    path('question/<int:qid>/', views.question ,name = 'question'),
    path('login/', views.login, name = 'login'),
    path('signup/', views.signup, name = 'signup'),
    path('settings/', views.settings, name = 'settings'),
    path('ask/', views.ask, name = 'ask'),
    path('hot/', views.hot_questions, name = 'hot'),
    path('tag/<str:tag_name>/', views.tag, name = 'tag'),
]

