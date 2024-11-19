# quiz/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('profile/', views.profile, name='profile'),
    path('previous_results/', views.previous_results, name='previous_results'),
    path('choose_category/', views.choose_category, name='choose_category'),
    path('category/<int:category_id>/question/', views.show_question, name='show_question'),
    path('question/<int:question_id>/answer/', views.answer_question, name='answer_question'),
    path('end_game/', views.end_game, name='end_game'),
    path('upload_questions/', views.upload_questions, name='upload_questions'),
    path('check_time/', views.check_time, name='check_time'),
]
