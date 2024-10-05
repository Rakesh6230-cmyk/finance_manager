from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Income(models.Model):
    CATEGORY_CHOICES = [
        ('Salary', 'Salary'),
        ('Bonus', 'Bonus'),
        ('Freelance', 'Freelance'),
        ('Investment', 'Investment'),
        ('Other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255, null=True)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')

    def __str__(self):
        return f"{self.category}: {self.description} - {self.amount}"

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Rent', 'Rent'),
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Bills', 'Bills'),
        ('Shopping', 'Shopping'),
        ('Other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Other')
    date = models.DateField()

    def __str__(self):
        return f"{self.category}: {self.description} - {self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.DateField()

    def __str__(self):
        return f"{self.category} - ${self.amount} for {self.month.strftime('%B %Y')}"
