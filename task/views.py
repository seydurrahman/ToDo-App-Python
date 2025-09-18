from django.shortcuts import render,redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

# # Create your views here.
@login_required
def task_list(request):
    status_filter = request.GET.get("status", "all")
    category_filter = request.GET.get("category", "all")

    tasks = Task.objects.filter(user=request.user)

    if status_filter != "all":
        tasks = tasks.filter(is_completed=(status_filter == "completed"))
    if category_filter != "all":
        tasks = tasks.filter(category=category_filter)

    completed_tasks = tasks.filter(is_completed=True).count()
    pending_tasks = tasks.filter(is_completed=False).count()

    return render(
        request,
        "task_list.html",
        {
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "status_filter": status_filter,
            "category_filter": category_filter,
            "tasks":tasks
        },
    )

@login_required
def task_create(request):
    if request.method== "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("task_list")
    else:
        form = TaskForm()
    return render(request,"task_form.html",{"form":form})
 
@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    return render(request,"task_detail.html",{"task":task})
@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        task.delete()
    return redirect("task_list")
@login_required
def task_mark_completed(request,task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_completed=True
    task.save()
    return redirect("task_list")

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect("task_list")
    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})







        







