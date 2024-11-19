# models.py

from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Question(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    text = models.TextField()
    correct_answer = models.CharField(max_length=100)
    choice_1 = models.CharField(max_length=100, default='default_choice')
    choice_2 = models.CharField(max_length=100, default='default_choice')
    choice_3 = models.CharField(max_length=100, default='default_choice')
    choice_4 = models.CharField(max_length=100, default='default_choice')

    def __str__(self):
        return self.text

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    stage = models.IntegerField(default=1)  # 1 for increasing, 2 for decreasing
    score = models.IntegerField(default=0)
    questions_answered = models.IntegerField(default=0)
    current_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(auto_now_add=True)

class GameResult(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    correct = models.BooleanField()
    points = models.IntegerField()
    time_answered = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female')), blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    def __str__(self):
        return self.user.username
