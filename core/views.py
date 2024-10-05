from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, IncomeForm, ExpenseForm, BudgetForm
from .models import Income, Expense, Budget
from django.db import models
from django.contrib.auth import logout
from django.db.models import Sum
from django.core.paginator import Paginator
from django.utils.timezone import now
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import BudgetForm
import json
from django.http import HttpResponse
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        # Check if the form is valid and the username doesn't already exist
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different one.")
            else:
                user = form.save()  # Save the user
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)  # Authenticate the user
                if user is not None:  # Check if the user is authenticated
                    login(request, user)  # Log the user in
                    messages.success(request, "Registration successful! You are now logged in.")
                    return redirect('dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            messages.success(request, "Login successful! Welcome back.")
            return redirect('dashboard')  # Redirect to dashboard after login
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    
    return render(request, 'login.html')
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logging out


@login_required
def dashboard(request):
    current_year = now().year
    current_month = now().month

    # Retrieve total income, expenses, and budgets for the user
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user, date__year=current_year, date__month=current_month)
    budgets = Budget.objects.filter(user=request.user, month__year=current_year, month__month=current_month)
    
    total_income = incomes.aggregate(Sum('amount'))['amount__sum'] or 0
    total_expenses = expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_budget = budgets.aggregate(Sum('amount'))['amount__sum'] or 0
    savings = total_income - total_expenses

    # Check if any budget is exceeded
    budget_notifications = []
    for budget in budgets:
        category_expenses = expenses.filter(category=budget.category).aggregate(Sum('amount'))['amount__sum'] or 0
        if category_expenses > budget.amount:
            budget_notifications.append({
                'category': budget.category,
                'spent': category_expenses,
                'limit': budget.amount
            })

    context = {
        'total_income': total_income,
        'total_expenses': total_expenses,
        'savings': savings,
        'total_budget': total_budget,
        'incomes': incomes,
        'expenses': expenses,
        'budgets': budgets,
        'current_year': current_year,
        'current_month': current_month,
        'budget_notifications': budget_notifications,
    }

    return render(request, 'dashboard.html', context)
# Add income
@login_required
def add_income(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('dashboard')
    else:
        form = IncomeForm()
    return render(request, 'add_income.html', {'form': form})
# Update Income
@login_required
def update_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = IncomeForm(instance=income)
    return render(request, 'edit_income.html', {'form': form})

# Delete Income
@login_required
def delete_income(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    if request.method == 'POST':
        income.delete()
        return redirect('dashboard')
    return render(request, 'delete_income.html', {'income': income})
def income_list(request):
    incomes = Income.objects.filter(user=request.user)
    return redirect('dashboard')
    # return render(request, 'income_list.html', {'incomes': incomes})
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})
# Update Expense
@login_required
def update_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'edit_expense.html', {'form': form})

# Delete Expense
@login_required
def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == 'POST':
        expense.delete()
        return redirect('dashboard')
    return render(request, 'delete_expense.html', {'expense': expense})

@login_required
def monthly_report(request, year, month):
    # Get income and expenses for the specific month and year
    incomes = Income.objects.filter(user=request.user, date__year=year, date__month=month).aggregate(total_income=Sum('amount'))
    expenses = Expense.objects.filter(user=request.user, date__year=year, date__month=month).aggregate(total_expenses=Sum('amount'))

    total_income = incomes['total_income'] or 0  # Default to 0 if None
    total_expenses = expenses['total_expenses'] or 0
    savings = total_income - total_expenses

    context = {
        'year': year,
        'month': month,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'savings': savings
    }

    return render(request, 'reports/monthly_report.html', context)
@login_required
def yearly_report(request, year):
    # Get income and expenses for the specific year
    incomes = Income.objects.filter(user=request.user, date__year=year).aggregate(total_income=Sum('amount'))
    expenses = Expense.objects.filter(user=request.user, date__year=year).aggregate(total_expenses=Sum('amount'))

    total_income = incomes['total_income'] or 0  # Default to 0 if None
    total_expenses = expenses['total_expenses'] or 0
    savings = total_income - total_expenses

    context = {
        'year': year,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'savings': savings
    }

    return render(request, 'reports/yearly_report.html', context)

@login_required
def add_budget(request):
    if request.method == 'POST':
        form = BudgetForm(request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            return redirect('dashboard')
    else:
        form = BudgetForm()
    return render(request, 'add_budget.html', {'form': form})

@login_required
def view_budget(request):
    # Get budgets for the logged-in user
    budgets = Budget.objects.filter(user=request.user)

    # Pagination
    paginator = Paginator(budgets, 10)  # Show 10 budgets per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Calculate totals for display (optional)
    total_budget_amount = sum(b.amount for b in budgets)

    return render(request, 'view_budget.html', {
        'page_obj': page_obj,
        'total_budget_amount': total_budget_amount,
        'budgets': budgets,
    })
    


def update_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk)
    if request.method == 'POST':
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('view_budget')  
    else:
        form = BudgetForm(instance=budget)
    return render(request, 'update_budget.html', {'form': form})
    
@login_required
def delete_budget(request, pk):
    budget = get_object_or_404(Budget, pk=pk, user=request.user)
    if request.method == 'POST':
        budget.delete()
        return redirect('view_budget')  # Redirect after deletion
    return render(request, 'delete_budget.html', {'budget': budget})  

            


@login_required
def backup_data(request):
    # Retrieve the user's data (Income, Expense, Budget)
    user_income = Income.objects.filter(user=request.user)
    user_expenses = Expense.objects.filter(user=request.user)
    user_budgets = Budget.objects.filter(user=request.user)

    # Serialize the data to JSON format
    data = {
        'income': serializers.serialize('json', user_income),
        'expenses': serializers.serialize('json', user_expenses),
        'budgets': serializers.serialize('json', user_budgets),
    }

    # Create JSON response to download the backup file
    response = HttpResponse(json.dumps(data), content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=backup.json'
    return response

    

logger = logging.getLogger(__name__)
@login_required
def restore_data(request):
    if request.method == 'POST' and request.FILES.get('backup_file'):
        backup_file = request.FILES['backup_file']
        try:
            # Load the JSON data
            data = json.load(backup_file)
            
            # Log the data structure to verify its format
            logger.debug(f"Backup data: {data}")

            # Access the income, expenses, and budgets data
            income_data = data.get('income', [])
            expense_data = data.get('expenses', [])
            budget_data = data.get('budgets', [])

            # Log individual structures for more granular verification
            logger.debug(f"Income data: {income_data}")
            logger.debug(f"Expense data: {expense_data}")
            logger.debug(f"Budget data: {budget_data}")

            # Restore income data
            for income in income_data:
                Income.objects.create(
                    user=request.user,
                    description=income['fields']['description'],
                    amount=income['fields']['amount'],
                    category=income['fields']['category'],
                    date=income['fields']['date'],
                )

            # Restore expense data
            for expense in expense_data:
                Expense.objects.create(
                    user=request.user,
                    description=expense['fields']['description'],
                    amount=expense['fields']['amount'],
                    category=expense['fields']['category'],
                    date=expense['fields']['date'],
                )

            # Restore budget data
            for budget in budget_data:
                Budget.objects.create(
                    user=request.user,
                    category=budget['fields']['category'],
                    amount=budget['fields']['amount'],
                    month=budget['fields']['month'],
                )

            return JsonResponse({'status': 'success', 'message': 'Data restored successfully!'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON file format'})
        except KeyError as e:
            logger.error(f"Key error: {e}")
            return JsonResponse({'status': 'error', 'message': f'Missing key: {str(e)}'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})



@login_required
def restore_data_page(request):
    return render(request, 'restore_data.html')