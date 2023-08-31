from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from .models import Task
from django.utils import timezone
# Create your views here.
# Home do projeto


def home(request):
    return render(request, 'menu.html')


def cadastro(request):

    if request.method == 'GET':
        return render(request, 'cadastrar.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                # Isso é um código q o próprio django tem de autenticação de usuário
                user = User.objects.create_user(
                    username=request.POST['email'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('login')
            except:

                return render(request, 'cadastrar.html', {
                    'form': UserCreationForm,
                    "error": 'Usuário já existe!'

                })
        return render(request, 'cadastrar.html', {
            'form': UserCreationForm,
            "error": 'Senhas incorreta'
        })


def logar(request):

    if request.method == 'GET':
        return render(request, 'login.html', {
            'form': AuthenticationForm
        })

    else:
        user = authenticate(
            request, username=request.POST['email'], password=request.POST['password'])

        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                "error": 'Usuário ou senha incorreto'
            })
        else:
            login(request, user)
            return redirect('tasks')


@login_required
def tasks(request):
    return render(request, 'tasks.html')


@login_required
def sair(request):
    logout(request)
    return redirect('home')


@login_required
def criando_tarefas(request):
    if request.method == 'GET':
        return render(request, 'criando_tarefas.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')

        except ValueError:
            return render(request, 'criando_tarefas.html', {
                'form': TaskForm,
                'error': 'Insira dados válidos'
            })


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})


@login_required
def task_detalhe(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detalhe.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(instance=task)
            form.save()
            return redirect('tasks')

        except ValueError:
            return render(request, 'task_detalhe.html', {'task': task, 'form': form,
                                                         'error': 'Erro ao atualizar uma Tarefa'
                                                         })


@login_required
def complete_tarefa(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)

    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def deletar_tarefa(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


@login_required
def exibir_tarefas_completadas(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})
