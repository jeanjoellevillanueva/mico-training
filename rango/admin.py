from django.contrib import admin
from rango.models import Category, Page 
from .models import Question, Choice
# Register your models here.

# Chapter 7 of tutorial of Writing your first Django app 
# focus on admin configuration
class ChoiceInline(admin.TabularInline): # Chapter 7 of tutorial
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin): # Chapter 7 of tutorial
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    #  list_display admin option, which is a tuple of field names to display, 
    #  as columns, on the change list page for the object
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date'] # Chapter 7 of tutorial

# For models and database exercise: Customizing the admin interface (Page model), 
# we will create a PageAdmin class that inherits from admin.ModelAdmin, 
# and we will specify the list_display attribute to display the title, category, 
# and url fields in the admin interface. 
# We will then register the Page model with the PageAdmin class to apply our customizations. 
# This code is like "Hey Django admin, when displaying the Page model, use these settings.
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url') 

# This code telling Django to “Make these models appear in the admin panel.”
admin.site.register(Category)
admin.site.register(Page, PageAdmin) 
admin.site.register(Question, QuestionAdmin)