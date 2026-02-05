from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Expense, Category
from .forms import ExpenseForm
from django.contrib.auth import logout
from .forms import CategoryForm

def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'register.html', {'form': form})

@login_required
def expense_list(request):
    expenses = Expense.objects.filter(user=request.user)
    total = sum(e.amount for e in expenses)
    return render(request, 'expense_list.html', {'expenses': expenses, 'total': total})

@login_required
def add_expense(request):
    form = ExpenseForm(request.POST or None)
    form.fields['category'].queryset = Category.objects.filter(user=request.user)
    if form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        return redirect('expense_list')
    return render(request, 'add_expense.html', {'form': form})

@login_required
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    form = ExpenseForm(request.POST or None, instance=expense)
    if form.is_valid():
        form.save()
        return redirect('expense_list')
    return render(request, 'edit_expense.html', {'form': form})

@login_required
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()
    return redirect('expense_list')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def add_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        category = form.save(commit=False)
        category.user = request.user
        category.save()
        return redirect('add_expense')
    return render(request, 'add_category.html', {'form': form})