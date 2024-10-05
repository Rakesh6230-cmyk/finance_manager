from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),  # Make sure this exists
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_income/', views.add_income, name='add_income'),
    path('update_income/<int:pk>/', views.update_income, name='update_income'),
    path('delete_income/<int:pk>/', views.delete_income, name='delete_income'),
    path('incomes/', views.income_list, name='income_list'),  # Add this line if it doesn't exist

    path('add_expense/', views.add_expense, name='add_expense'),
    path('add_budget/', views.add_budget, name='add_budget'),
    path('update_expense/<int:pk>/', views.update_expense, name='update_expense'),
    path('delete_expense/<int:pk>/', views.delete_expense, name='delete_expense'),
    path('reports/monthly/<int:year>/<int:month>/', views.monthly_report, name='monthly_report'),
    path('reports/yearly/<int:year>/', views.yearly_report, name='yearly_report'),
    path('view_budget/', views.view_budget, name='view_budget'),
    path('budget/update/<int:pk>/', views.update_budget, name='update_budget'),
    path('budget/delete/<int:pk>/', views.delete_budget, name='delete_budget'),
    path('logout/', views.logout_view, name='logout'),
    path('backup/', views.backup_data, name='backup_data'),
    path('restore/', views.restore_data, name='restore_data'),
    path('restore/', views.restore_data_page, name='restore_data_page'),  # Page to upload backup
    path('restore_data/', views.restore_data, name='restore_data'),  # View to handle restore functionality
]
