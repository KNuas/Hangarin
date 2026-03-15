from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, SubTask, Note, Category, Priority
from .forms import TaskForm


def dashboard(request):
    tasks = Task.objects.all().order_by('-created_at')[:5]
    total_tasks = Task.objects.count()
    pending_tasks = Task.objects.filter(status="Pending").count()
    in_progress_tasks = Task.objects.filter(status="In Progress").count()
    completed_tasks = Task.objects.filter(status="Completed").count()

    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
    }

    return render(request, 'tasks/dashboard.html', context)


def task_list(request):

    sort = request.GET.get('sort')

    tasks = Task.objects.all()

    if sort == "date":
        tasks = tasks.order_by('-created_at')

    elif sort == "priority":
        tasks = tasks.order_by('priority__name')

    elif sort == "status":
        tasks = tasks.order_by('status')

    elif sort == "title":
        tasks = tasks.order_by('title')

    context = {
        'tasks': tasks
    }

    return render(request, 'tasks/task_list.html', context)

def dashboard(request):
    sort = request.GET.get('sort')

    tasks = Task.objects.all()

    if sort == "date":
        tasks = tasks.order_by('-created_at')
    elif sort == "deadline":
        tasks = tasks.order_by('deadline')
    elif sort == "status":
        tasks = tasks.order_by('status')
    elif sort == "priority":
        tasks = tasks.order_by('priority__name')
    else:
        tasks = tasks.order_by('-created_at')

    tasks = tasks[:5]

    total_tasks = Task.objects.count()
    pending_tasks = Task.objects.filter(status="Pending").count()
    in_progress_tasks = Task.objects.filter(status="In Progress").count()
    completed_tasks = Task.objects.filter(status="Completed").count()

    context = {
        'tasks': tasks,
        'total_tasks': total_tasks,
        'pending_tasks': pending_tasks,
        'in_progress_tasks': in_progress_tasks,
        'completed_tasks': completed_tasks,
    }

    return render(request, 'tasks/dashboard.html', context)


def task_detail(request, pk):

    task = get_object_or_404(Task, pk=pk)

    subtasks = SubTask.objects.filter(parent_task=task)

    notes = Note.objects.filter(task=task)

    context = {
        'task': task,
        'subtasks': subtasks,
        'notes': notes,
    }

    return render(request, 'tasks/task_detail.html', context)


def task_create(request):

    if request.method == 'POST':

        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('task_list')

    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Add Task'
    })


def task_update(request, pk):

    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':

        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('task_detail', pk=task.pk)

    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'title': 'Edit Task'
    })


def task_delete(request, pk):

    task = get_object_or_404(Task, pk=pk)

    if request.method == 'POST':

        task.delete()

        return redirect('task_list')

    return render(request, 'tasks/task_confirm_delete.html', {
        'task': task
    })

def subtask_list(request):

    search = request.GET.get('search')
    status = request.GET.get('status')

    subtasks = SubTask.objects.all().order_by('-created_at')

    if search:
        subtasks = subtasks.filter(title__icontains=search)

    if status:
        subtasks = subtasks.filter(status=status)

    context = {
        "subtasks": subtasks
    }

    return render(request, "tasks/subtask_list.html", context)

def mark_task_completed(request, pk):

    task = get_object_or_404(Task, pk=pk)

    task.status = "Completed"

    task.save()

    return redirect('task_list')

def note_list(request):
    search = request.GET.get('search')
    created_at = request.GET.get('created_at')

    notes = Note.objects.all().order_by('-created_at')

    if search:
        notes = notes.filter(content__icontains=search)

    if created_at:
        notes = notes.filter(created_at__date=created_at)

    context = {
        "notes": notes
    }

    return render(request, "tasks/note_list.html", context)

def category_list(request):
    search = request.GET.get('search')

    categories = Category.objects.all().order_by('name')

    if search:
        categories = categories.filter(name__icontains=search)

    context = {
        "categories": categories
    }

    return render(request, "tasks/category_list.html", context)