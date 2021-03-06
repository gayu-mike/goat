# from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from lists.forms import TodoForm, ExistingListTodoForm, NewListForm
from lists.models import Todo, List
from utils import log


User = get_user_model()


def home_page(request):
    form = TodoForm()
    return render(request, 'lists/home_page.html', {'form': form})


def new_list(request):
    form = NewListForm(data=request.POST)
    if form.is_valid():
        ls = form.save(user=request.user)
        return redirect(ls)
    return render(request, 'lists/home_page.html', {'form': form})


def view_list(request, list_id):
    ls = List.objects.get(id=list_id)
    form = ExistingListTodoForm(for_list=ls)
    if request.method == 'POST':
        form = ExistingListTodoForm(for_list=ls, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(ls)

    todos = Todo.objects.filter(list=ls)
    context = {
        'list': ls,
        'todos': todos,
        'form': form
    }
    return render(request, 'lists/list.html', context)


def my_lists(request, email):
    user = User.objects.get(email=email)
    return render(request, 'lists/my_lists.html', {'user': user})
