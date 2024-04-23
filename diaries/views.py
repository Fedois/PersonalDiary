from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.urls import reverse
from datetime import timedelta, datetime
from django.contrib import messages
import json
import re
from .models import User, Diary, Todo

# AUTH USER.
def login_user(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'login.html', {
                'message': 'Invalid username and/or password'
            })
    else: 
        return render(request, 'login.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirm']

        if password != confirmation: 
            return render(request, 'register.html', {
                'message': 'Passwords must match'
            })
        
        if email != '':
            valid_email = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
            if not valid_email: 
                return render(request, 'register.html', {
                    'message' : 'Not valid email'
                })
        
        try: 
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'register.html', {
                'message': 'Username already taken'
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'register.html')

def logout_user(request):
    logout(request)
    return render(request, 'login.html')


# PROJECT VIEWS
def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html', {
            'diaries' : Diary.objects.filter(user = request.user)
        })
    else:
        return render(request, 'login.html')

def show(request, id):
    if request.user.is_authenticated:
        diary = Diary.objects.get(pk = id)
        day_one = datetime.now().date()
        day_two = day_one + timedelta(1)

        return render(request, 'show.html', {
            'diaries': Diary.objects.filter(user = request.user),
            'diary': diary,
            'data_title_sx': day_one,
            'data_title_dx': day_two,
            'todos_sx': diary.todos.filter(date = day_one),
            'todos_dx' : diary.todos.filter(date = day_two)
        })
    else:
        return render(request, 'login.html')

def create_diary(request):
    if request.method == 'POST' and request.POST['name'] != '':
        diary = Diary(name = request.POST['name'], user = request.user)
        diary.save()

        messages.success(request, 'Diary created successfully!')

        return HttpResponseRedirect(reverse('index'))

def create_todo(request, id):
    if request.method == 'POST':
        try:
            important = True if request.POST['is_important'] == 'on' else False
            print(request.POST['is_important'])
        except:
            important = False
        diary = Diary.objects.get(pk = id)
        todo = Todo(title = request.POST['title'], description = request.POST['description'], date = request.POST['date'], is_important = important, diary = diary)
        todo.save()

        messages.success(request, 'Todo created successfully!')

        return HttpResponseRedirect(reverse('show', args=[id]))

def next_page(request, id):
    diary = Diary.objects.get(pk = id)

    try: 
        request_date = request.GET['date'] 
        date = datetime.strptime(request_date, "%B %d, %Y").date()
        day_one = date + timedelta(1)
        day_two = day_one + timedelta(1)
    except:
        request_date = request.GET['date_mobile']
        date = datetime.strptime(request_date, "%B %d, %Y").date()
        day_one = date
        day_two = day_one + timedelta(1)

    return render(request, 'show.html', {
            'diaries': Diary.objects.filter(user = request.user),
            'diary': diary,
            'data_title_sx': day_one,
            'data_title_dx': day_two,
            'todos_sx': diary.todos.filter(date = day_one),
            'todos_dx' : diary.todos.filter(date = day_two)
    })

def back_page(request, id):
    diary = Diary.objects.get(pk = id)

    try: 
        date = datetime.strptime(request.GET['date'], "%B %d, %Y").date()
        day_two = date - timedelta(1)
        day_one = day_two - timedelta(1)
    except:
        date = datetime.strptime(request.GET['date_mobile'], "%B %d, %Y").date()
        day_two = date
        day_one = day_two - timedelta(1)

    return render(request, 'show.html', {
            'diaries': Diary.objects.filter(user = request.user),
            'diary': diary,
            'data_title_sx': day_one,
            'data_title_dx': day_two,
            'todos_sx': diary.todos.filter(date = day_one),
            'todos_dx' : diary.todos.filter(date = day_two)
        })

# API
def todo_done(request, id):
    todo = Todo.objects.get(pk = id)
    if request.method == 'PUT': 
        is_done = False if todo.done else True
        todo.done = is_done
        todo.save()
        return  JsonResponse({'done': todo.done}, status=200)

def edit_todo(request, id):
    todo = Todo.objects.get(pk = id)
    if request.method == 'PUT':
        data = json.loads(request.body)
        if data['title'] == '' or data['description'] == '':
            return JsonResponse({'error' : 'title and description are required'})
        else: 
            todo.title = data['title']
            todo.description = data['description']
            todo.save()
            return JsonResponse({'message' : 'todo edited successfully'})

def delete_todo(request, id):
    if request.method == 'DELETE':
        todo = Todo.objects.get(pk = id)
        todo.delete()
        return JsonResponse({'message' : 'todo deleted successfully'})
