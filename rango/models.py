import datetime 
import re
from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django import forms
from django.contrib.auth.models import User


# From Django tutorial 
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text
    
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
##############

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    # We want to be able to query the number of views and likes a category has.
    # We can use the IntegerField field type to store this information, and set the default value to 0.
    # This means that when we create a new category, it will have 0 views and 0 likes by default.
    # This is Chapter 5 of Tango with Django, and we will be adding this code to our models.py file.
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    date_added = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name
   
class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title 
    
#This block of code is used to clean and fix the URL before saving it.
#Its main job is:
#“Make sure every URL starts with https://.”
class PageForm(forms.ModelForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        # Strip away any leading http or https 
        url =re.sub(r'^https?://', '', url)
        # If url is not empty and doesn't start with 'https://',
        # then prepend 'https://' as we want to make sure
        # we are accessing a secure site
        if url: 
            url = f'https://{url}'
            cleaned_data['url'] = url
        return cleaned_data
    
# Chapter 9.4 User Model 
class UserProfile(models.Model):
    # This line is required. Link UserProfile to a User model instance.
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    
## When adding a features Step 1 (Add A Bookmark Model)
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    date_saved = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'page')
        ordering = ['-date_saved']

    def __str__(self):
        return f'{self.user.username} saved {self.page.title}'
    
class BrokenLinkReport(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.TextField(blank=True)
    date_reported = models.DateTimeField(default=timezone.now)
    resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_reported']

    def __str__(self):
        return f'{self.page.title} reported by {self.user.username}'
    

class LearningNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True)

    title = models.CharField(max_length=128)
    concept = models.CharField(max_length=128)
    explanation = models.TextField()
    code_example = models.TextField(blank=True)

    reviewed = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['reviewed', '-date_added']

    def __str__(self):
        return self.title
