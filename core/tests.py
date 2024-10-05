from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Income, Expense
from django.core.files.uploadedfile import SimpleUploadedFile
import json


class UserRegistrationTest(TestCase):
    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'password1': 'password123',
            'password2': 'password123',
        })
        
        # Check if the registration passed validation
        if response.status_code == 200:
            self.fail("Form submission failed. Check form errors: " + str(response.context['form'].errors))
        
        self.assertEqual(response.status_code, 302)  # Expecting a redirect after successful registration
        self.assertTrue(User.objects.filter(username='testuser').exists())  # Ensure user was created

class IncomeExpenseTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_add_income(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('add_income'), {
            'description': 'Salary',
            'amount': 5000,
            'category': 'Salary',
            'date': '2024-10-04'
        })
        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertTrue(Income.objects.filter(user=self.user, description='Salary').exists())

    def test_add_expense(self):
        self.client.login(username='testuser', password='password')
        response = self.client.post(reverse('add_expense'), {
            'description': 'Groceries',
            'amount': 100,
            'category': 'Food',
            'date': '2024-10-04'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Expense.objects.filter(user=self.user, description='Groceries').exists())

class BackupRestoreTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_restore_data(self):
        self.client.login(username='testuser', password='password')
        # Simulate a backup file upload
        backup_file = SimpleUploadedFile("backup.json", json.dumps({'data': 'backup_data'}).encode())
        response = self.client.post(reverse('restore_data'), {'backup_file': backup_file})
        self.assertEqual(response.status_code, 302)
        # Add more assertions depending on your restore logic
