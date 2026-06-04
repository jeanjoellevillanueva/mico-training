from multiprocessing import context
from unicodedata import category
from urllib import request, response
from django.shortcuts import render, redirect
from django.http import HttpResponse
from rango.models import Category, Page, UserProfile
from rango.forms import  CategoryForm, PageForm
from django.urls import reverse
from rango.forms import UserForm, UserProfileForm 
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from rango.search import run_query

def show_category(request, category_name_slug):
    # Create a context dictionary which we can pass
    # to the template rendering engine.
    context_dict = {}
    try:
        # Can we find a category name slug with the given name?
        # If we can't, the .get() method raises a DoesNotExist exception.
        # The .get() method returns one model instance or raises an exception.
        category = Category.objects.get(slug=category_name_slug)
        
        # Retrieve all of the associated pages.
        # The filter() will return a list of page objects or an empty list.
        # order_by('-views') will order the pages by the number of views in descending order.
        pages = Page.objects.filter(category=category).order_by('-views')

        # Adds our results list to the template context under name pages.
        context_dict['pages'] = pages
        # We also add the category object from
        # the database to the context dictionary.
        # We'll use this in the template to verify that the category exists.
        context_dict['category'] = category

        context_dict['result_list'] = []
        context_dict['query'] = ''

        if request.method == 'POST':
            if not request.user.is_authenticated:
                return redirect('accounts:login')
        
         # NEW: handle search
            query = request.POST.get('query', '').strip()
            context_dict['query'] = query

            if query:
                # example search logic (replace with your real search)
                result_list = run_query(query)  # your existing search function
                context_dict['result_list'] = result_list
                
    except Category.DoesNotExist:
        # We get here if we didn't find the specified category.
        # Don't do anything -
        # the template will display the "no category" message for us.
        context_dict['category'] = None
        context_dict['pages'] = None

    # Go render the response and return it to the client.   
    return render(request, 'rango/category.html', context=context_dict)

# Remember that the index() function is responsible for the main page view.
def index(request):
    # Query the database for a list of ALL categories currently stored.
    # Order the categories by the number of likes in descending order.
    # Retrieve the top 5 only -- or all if less than 5. 
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    # Place the list in our context_dict dictionary (with our boldmessage!)
    # that will be passed to the template engine.
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    # IMPORTANT: use session not cookies 
    context_dict['visits'] = int(request.session.get('visits', '1'))

    # Obtain our Response object early so we can add cookie information.
    response = render(request, 'rango/index.html', context=context_dict)

    # Call the helper function to handle the cookies
    response = visitor_cookies_handler(request, response)

    # Return response back to the user, updating any cookies that need changed.
    return response

def about(request):
    # prints out whether the method is a GET or a POST
    print(request.method)
    # prints out the user name, if no one is logged in it prints `AnonymousUser`
    print(request.user)

    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()

    # return render(request, 'rango/about.html', {})
    visits = request.session.get('visits', 1)
    return render(request, 'rango/about.html', {'visits': visits})



# Creating an Add Category View
# Create a new view to display the form
# and handle the posting of form data.
@login_required
def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now call the index() view.
            # The user will be shown the homepage.
            return redirect('/rango/')
        else:
            # The supplied form contained errors - 
            # just print them to the terminal.
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # You cannot add a page to a Category that does not exist...
    if category is None:
        return redirect(reverse('rango:index'))
    
    form = PageForm() 
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        print(form.errors)

    return render(request, 'registration/registration_form.html', {'form': form})

    
@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
        val = request.session.get(cookie)
        if not val:
            val = default_val
        return val

def visitor_cookies_handler(request, response):
        #Get the number of visits to the site.
        # We use the COOKIES.get() function to obtain the visits cookie.
        # If the cookie exists, the value returned is casted to an integer.
        # If the cookie doesn't exist, then the default value of 1 is used.
        visits = request.session.get('visits', '1')

        last_visit = request.session.get('last_visit')

        current_time = datetime.now()

        if last_visit:
            last_visit_time = datetime.strptime(last_visit, '%Y-%m-%d %H:%M:%S.%f')

            # If more than a day passed
            if (current_time - last_visit_time).days > 0:
                visits += 1
            
        else:
            visits = 1

        # Update/set the visits cookie
        request.session['visits'] = visits
        request.session['last_visit'] = str(current_time)

        return response

# def search(request):
#     result_list = []
#     query = ''

#     if request.method == 'POST':
#         query = request.POST.get('query', '').strip()

#         if query:
#         # Run our Bing function to get the results list!
#             result_list = run_query(query)

#     return render(request, 'rango/search.html', 
#                   {'result_list': result_list, 
#                    'query': query
#                    }
#               ) 

def goto_url(request):
    page_id = None
    url = '/rango/'

    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']

            try:
                page = Page.objects.get(id=page_id)

                page.views += 1
                page.save()

                url = page.url

            except Page.DoesNotExist:
                pass

    return redirect(url)

def register_profile(request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('index')
        else:
            print(form.errors)

    return render(request, 'registration/profile_registration.html', {'form': form})

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    context_dict = {'user_profile': user_profile}
    return render(request, 'rango/profile.html', context=context_dict)

