from django.db import models
# From Django tutorial 
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
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


    class Meta:
        verbose_name_plural = 'Categories'
        
    def __str__(self):
        return self.name
   
class Page(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title 