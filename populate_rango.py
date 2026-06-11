import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                     'tango_with_django_project.settings')
import django
django.setup()
from rango.models import Category, Page

def populate():
# First, we will create lists of dictionaries containing the pages
# we want to add into each category.
# Then we will create a dictionary of dictionaries for our categories.
# This might seem a little bit confusing, but it allows us to iterate
# through each data structure, and add the data to our models.

    python_pages = [
        {'title': 'Official Python Tutorial',
        'url':'http://docs.python.org/3/tutorial/',
        'views': 100},
        {'title':'How to Think like a Computer Scientist',
        'url':'http://www.greenteapress.com/thinkpython/',
        'views': 50},
        {'title':'Learn Python in 10 Minutes',
        'url':'http://www.korokithakis.net/tutorials/python/',
        'views': 25} ]
    
    django_pages = [
        {'title':'Official Django Tutorial',
        'url':'https://docs.djangoproject.com/en/4.0/intro/tutorial01/',
        'views': 100},
        {'title':'Django Rocks',
        'url':'http://www.djangorocks.com/',
        'views': 50},
        {'title':'How to Tango with Django',
        'url':'http://www.tangowithdjango.com/',
        'views': 25} ]
    
    other_pages = [
        {'title':'Bottle',
        'url':'http://bottlepy.org/docs/dev/',
        'views': 100},
        {'title':'Flask',
        'url':'http://flask.pocoo.org',
        'views': 50} ]
    
    cats = {'Python': {'pages': python_pages},
            'Django': {'pages': django_pages},
            'Other Frameworks': {'pages': other_pages},
            'Pascal': {'pages': []},
            'Perl': {'pages': []},
            'PHP': {'pages': []},
            'Prolog': {'pages': []},
            'PostScript': {'pages': []},
            'Programming': {'pages': []}, }
    


# If you want to add more categories or pages,
# add thjem to the dictionaries above.

# The code below goes through the cat dictionary, then adds each category,
# add then adds all the associated pages for that category.
    for cat, cat_data in cats.items():
        c = add_cat(cat)
        for p in cat_data['pages']:
            add_page(c, p['title'], p['url'])

# Print out the categories we have added.
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views=0):
    # get_or_create = "find it or make it"
    # save = "write it into the database"
    # return = "give me the result back"

    p, created = Page.objects.get_or_create(
        category=cat,
        title=title,
        defaults={'url': url, 'views': views}
    )
    p.save()
    return p

def add_cat(name):
    # Each category has a default number of views and likes associated with it.
    # Exercise: Add more categories and pages to populate() and add appropriate number of views and likes to each category.
    # Simple logic for the number of views and likes for each category.
    if name == 'Python':
        views = 128
        likes = 64
    elif name == 'Django':
        views = 64
        likes = 32
    elif name == 'Other Frameworks':
        views = 32
        likes = 16
    else:
        views = 32
        likes = 16
    ###########################
    c = Category.objects.get_or_create(name=name)[0]
    c.save()
    return c

# Start execution here!

if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()

