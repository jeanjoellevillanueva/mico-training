from django.contrib import admin
from .models import Question, Choice
from rango.models import UserProfile, Category, Page, Bookmark

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

# customise the admin interface so that it automatically pre-populates
# the slug field as you type in the category name.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} 

# When adding a features Step 2 (Register It In Admin)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'page', 'date_saved')
    list_filter = ('date_saved',)
    search_fields = ('user__username', 'page__title')

# This code telling Django to “Make these models appear in the admin panel.”
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin) 
admin.site.register(Question, QuestionAdmin)
admin.site.register(UserProfile)
admin.site.register(Bookmark, BookmarkAdmin)