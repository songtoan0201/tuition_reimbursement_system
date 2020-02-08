from django.db import models
import datetime
import re
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)


class EmployerManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['company_name']) < 2:
            errors["company_name"] = "Company name should be at least 2 characters"
        if len(postData['password']) < 6:
            errors["password"] = "Password should be at least 6 characters"
        if postData['confirm_PW'] != postData['password']:
            errors["confirm_PW"] = "Password doesn't match"
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(postData['email']) or len(postData['email']) == 0:
            errors['email'] = "Invalid email address!"
        return errors


class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['password']) < 6:
            errors["password"] = "Password should be at least 6 characters"
        if postData['confirm_PW'] != postData['password']:
            errors["confirm_PW"] = "Password doesn't match"
        if not len(postData['phone_no']) == 10:
            errors["phone_no"] = "Phone number is invalid"
        if postData['birthday'] > datetime.datetime.now().strftime('%Y-%m-%d'):
            errors["birthday"] = "Birthday should be in the past"

        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(postData['email']) or len(postData['email']) == 0:
            errors['email'] = "Invalid email address!"
        return errors


class Employer(models.Model):
    company_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EmployerManager()


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField()
    phone_no = models.IntegerField(null=True)
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    employer = models.ForeignKey(
        Employer, related_name="employees",  on_delete=models.PROTECT)

    objects = UserManager()
