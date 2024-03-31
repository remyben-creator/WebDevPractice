from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.db import connection

from .models import Todo

# Create your views here.

def index(request):
    todos = Todo.objects.all()
    return render(request, "base.html", {"todos": todos})

def reset_sequence():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='todolist_todo'")

@require_http_methods(["POST"])
def add(request):
    title = request.POST["title"]
    todo = Todo(title=title)
    todo.save()
    return redirect("index")

def update(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.complete = not todo.complete
    todo.save()
    return redirect("index")

def delete(request, todo_id):
    todo = Todo.objects.get(id=todo_id)
    todo.delete()
    if not Todo.objects.exists():
        reset_sequence()
    return redirect("index")
