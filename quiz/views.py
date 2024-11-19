import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Category, Question, Game, GameResult
from .forms import SignUpForm, LoginForm, UploadFileForm
import pandas as pd
from django.utils import timezone
import random
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
import jdatetime
from django_jalali.forms import jDateField
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

def home(request):
    return render(request, 'index1.html')


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'age', 'gender', 'phone_number', 'profile_picture')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('birth_date', 'gender', 'profile_picture')

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)  # ایجاد پروفایل کاربر جدید
            login(request, user)
            return redirect('profile')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})

@login_required
def previous_results(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    games = Game.objects.filter(user=request.user).order_by('-start_time')
    
    if start_date and end_date:
        start_date = jdatetime.datetime.strptime(start_date, '%Y-%m-%d').togregorian()
        end_date = jdatetime.datetime.strptime(end_date, '%Y-%m-%d').togregorian()
        games = games.filter(start_time__range=(start_date, end_date))
    
    return render(request, 'previous_results.html', {'games': games})



@login_required
def show_question(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    questions = Question.objects.filter(category=category).order_by('?')
    if questions.exists():
        question = questions.first()
        choices = [
            question.correct_answer,
            question.choice_1,
            question.choice_2,
            question.choice_3,
            question.choice_4
        ]
        random.shuffle(choices)

        # Set timer
        request.session['start_time'] = timezone.now().timestamp()
        request.session['end_time'] = (timezone.now() + datetime.timedelta(seconds=25)).timestamp()

        context = {
            'question': question,
            'choices': choices,
            'category': category,
            'end_time': request.session['end_time']
        }
        return render(request, 'show_question.html', context)
    else:
        return render(request, 'no_questions.html', {'category': category})

@login_required
def check_time(request):
    end_time = request.session.get('end_time', None)
    if end_time:
        current_time = timezone.now().timestamp()
        time_left = end_time - current_time
        if time_left <= 0:
            return JsonResponse({'time_up': True})
        return JsonResponse({'time_up': False, 'time_left': int(time_left)})
    return JsonResponse({'time_up': True})
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('choose_category')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('choose_category')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def choose_category(request):
    categories = Category.objects.all()
    return render(request, 'choose_category.html', {'categories': categories})




@login_required
def answer_question(request, question_id):
    # ایجاد یا دریافت بازی
    game, created = Game.objects.get_or_create(user=request.user, current_question_id=question_id)
    question = get_object_or_404(Question, pk=question_id)
    choices = [
        question.correct_answer,
        question.choice_1,
        question.choice_2,
        question.choice_3,
        question.choice_4
    ]
    random.shuffle(choices)
    if request.method == 'POST':
        answer = request.POST.get('answer')
        correct = answer == question.correct_answer
        points = 0
        if correct:
            if game.stage == 1:
                points = random.randint(1, 6)  # Simulating dice roll for stage 1
            else:
                points = -random.randint(1, 6)  # Simulating dice roll for stage 2

        game_result = GameResult.objects.create(
            game=game,
            question=question,
            correct=correct,
            points=points,
            time_answered=timezone.now()
        )

        game.score += points
        game.questions_answered += 1
        game.current_question = None
        game.save()

        if correct:
            message = f'Correct! You {"gained" if game.stage == 1 else "lost"} {abs(points)} points.'
        else:
            message = f'Wrong! You {"gained" if game.stage == 1 else "lost"} 0 points.'

        return render(request, 'answer_result.html', {'message': message, 'category_id': question.category.id})

    return render(request, 'answer_question.html', {'question': question, 'choices': choices})




@login_required
def end_game(request):
    return render(request, 'end_game.html')

@login_required
def upload_questions(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            data = pd.read_excel(file)
            for index, row in data.iterrows():
                category, created = Category.objects.get_or_create(name=row['Category'])
                Question.objects.create(
                    category=category,
                    text=row['Question'],
                    correct_answer=row['CorrectAnswer'],
                    choice_1=row['Choice1'],
                    choice_2=row['Choice2'],
                    choice_3=row['Choice3'],
                    choice_4=row['Choice4']
                )
            return redirect('admin:index')
    else:
        form = UploadFileForm()
    return render(request, 'upload_questions.html', {'form': form})


