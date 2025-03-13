from audioop import reverse

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.utils.timezone import now
from .forms import TaskForm
from .models import Task

from datetime import timedelta


def home(request):
    tasks = Task.objects.filter(user=request.user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_completed=True).count()
    in_progress_tasks = tasks.filter(is_completed=False).count()

    overdue_tasks = tasks.filter(due_date__lt=now(), is_completed=False).count()
    due_soon_tasks = tasks.filter(due_date__gte=now(), due_date__lte=now() + timedelta(days=3),
                                  is_completed=False).count()
    due_later_tasks = tasks.filter(due_date__gt=now() + timedelta(days=3), is_completed=False).count()
    nearest_task = tasks.filter(is_completed=False, due_date__isnull=False).order_by('due_date').first()

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'in_progress_tasks': in_progress_tasks,
        'overdue_tasks': overdue_tasks,
        'due_soon_tasks': due_soon_tasks,
        'due_later_tasks': due_later_tasks,
        'nearest_task': nearest_task,
    }

    return render(request, 'main/home.html', context)


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'main/register.html', {'form': form})


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    return redirect('home')


@login_required
def tasks_view(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'main/tasks.html', {'tasks': tasks})


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('tasks')
    else:
        form = TaskForm()

    return render(request, 'main/add_task.html', {'form': form})


@login_required
def task_detail(request, task_id):
    try:
        task = Task.objects.get(id=task_id, user=request.user)
    except Task.DoesNotExist:
        return HttpResponse("Task not found", status=404)

    return render(request, 'main/task_detail.html', {'task': task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('tasks')


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed = not task.is_completed
    task.save()
    return redirect('tasks')


def custom_404(request, exception):
    return render(request, 'main/404.html', status=404)


def custom_500(request):
    return render(request, 'main/500.html', status=500)
