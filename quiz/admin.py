# quiz/admin.py

from django.contrib import admin
from .models import Category, Question, Game, GameResult

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'category')
    fields = ('category', 'text', 'correct_answer', 'choice_1', 'choice_2', 'choice_3', 'choice_4')

admin.site.register(Category)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Game)
admin.site.register(GameResult)
