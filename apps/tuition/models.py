from django.db import models
from django.shortcuts import render, redirect
import datetime
from apps.login.models import *
import re
# from db_file_storage.model_utils import delete_file, delete_file_if_needed
# from db_file_storage.form_widgets import DBClearableFileInput
from django.core.files.storage import FileSystemStorage

class ApplicationManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['institution']) == 0:
            errors["no_institution"] = "Institution must be provided"
        if len(postData['start_date']) == 0:
            errors["no_start_date"] = "Start Date must be provided"
        if len(postData['end_date']) == 0:
            errors["no_end_date"] = "End date must be provided"
        if len(postData['course_name']) == 0:
            errors["no_course_name"] = "Course name must be provided"
        if len(postData['cost']) == 0:
            errors["no_cost"] = "Cost must be provided"
        if postData['start_date'] < datetime.datetime.now().strftime('%Y-%m-%d'):
            errors["start_date"] = "Start date should be in the future"
        if postData['end_date'] < postData['start_date']:
            errors["end_date"] = "End date should be after start date"
        return errors
    
# application_file = FileSystemStorage(location='/media')

class Application(models.Model):
    institution = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    course_name = models.CharField(max_length=255)
    cost = models.IntegerField()
    other_fees = models.IntegerField(blank=True, null=True, default=0)
    total_cost = models.IntegerField(blank=True, null=True)
    add_info = models.TextField(blank=True, null=True)

    application_file = models.ImageField(upload_to='', blank=True, null=True)

    is_pending = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    add_info_required = models.BooleanField(default=False)
    is_rejected != is_approved
    amount_awarded = models.IntegerField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="applications")
    objects = ApplicationManager()

    # def save(self, *args, **kwargs):
    #     delete_file_if_needed(self, 'file')
    #     super(Application, self).save(*args, **kwargs)

    # def delete(self, *args, **kwargs):
    #     super(Application, self).delete(*args, **kwargs)
    #     delete_file(self, 'file')


class ApplicationFile(models.Model):
    bytes = models.TextField()
    filename = models.CharField(max_length=255)
    mimetype = models.CharField(max_length=50)

  