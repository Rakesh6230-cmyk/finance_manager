# Generated by Django 5.1.1 on 2024-10-04 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_income_category_expense_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='income',
            name='category',
            field=models.CharField(choices=[('Salary', 'Salary'), ('Bonus', 'Bonus'), ('Freelance', 'Freelance'), ('Investment', 'Investment'), ('Other', 'Other')], default='Other', max_length=50),
        ),
        migrations.AlterField(
            model_name='expense',
            name='category',
            field=models.CharField(choices=[('Rent', 'Rent'), ('Food', 'Food'), ('Travel', 'Travel'), ('Bills', 'Bills'), ('Shopping', 'Shopping'), ('Other', 'Other')], default='Other', max_length=50),
        ),
        migrations.AlterField(
            model_name='expense',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='expense',
            name='description',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='income',
            name='description',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
