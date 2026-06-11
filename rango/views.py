from urllib import request, response

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.views.generic import TemplateView, ListView

from django.urls import reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from datetime import datetime

from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from rango.search import run_query

class ShowCategoryView(View):

    def get_category(self, category_name_slug):
        try:
            return Category.objects.get(slug=category_name_slug)
        except Category.DoesNotExist:
            return None

    def get(self, request, category_name_slug):   
            
        category = self.get_category(category_name_slug)

        context_dict = {
            'category': category,
            'pages': None,
            'result_list': [],
            'query': ''   
        }

        if category:
            pages = Page.objects.filter(category=category).order_by('-views')
            context_dict['pages'] = pages

        return render(request, 'rango/category.html', context=context_dict)
    
    def post(self, request, category_name_slug):

        category = self.get_category(category_name_slug)

        if category is None:
            return redirect(reverse('rango:index'))
        
        query = request.POST.get('query', '').strip()
        context_dict = {
            'category': category,
            'pages': Page.objects.filter(category=category).order_by('-views'),
            'result_list': [],
            'query': query
        }

        if not request.user.is_authenticated:
            return redirect('accounts:login')
        
        if query:
            context_dict['result_list'] = run_query(query)
           
        return render(request, 'rango/category.html', context=context_dict)




class IndexView(View):

    def get(self, request):

        category_list = Category.objects.order_by('-likes')[:5]
        page_list = Page.objects.order_by('-views')[:5]
        
        context_dict = {
            'boldmessage:': 'Crunchy, creamy, cookie, candy, cupcake!',
            'categories': category_list,
            'pages': page_list,
            'visits': int(request.session.get('visits', '1')) # IMPORTANT: use session not cookies
        }
        
        # Obtain our Response object early so we can add cookie information.
        response = render(request, 'rango/index.html', context=context_dict)

        # Call the helper function to handle the cookies
        response = visitor_cookies_handler(request, response)

        # Return response back to the user, updating any cookies that need changed.
        return response


# def about(request):
#     # prints out whether the method is a GET or a POST
#     print(request.method)
#     # prints out the user name, if no one is logged in it prints `AnonymousUser`
#     print(request.user)

#     if request.session.test_cookie_worked():
#         print("TEST COOKIE WORKED!")
#         request.session.delete_test_cookie()

#     # return render(request, 'rango/about.html', {})
#     visits = request.session.get('visits', 1)
#     return render(request, 'rango/about.html', {'visits': visits})


# Creating an Add Category View
# Create a new view to display the form
# and handle the posting of form data.

class AddCategoryView(View):

    def get(self, request):
        form = CategoryForm()
        return render(request, 'rango/add_category.html', {'form': form})

    def post(self, request):
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



class AddPageView(View):
    def get_category(self, category_name_slug):
        try:
            return Category.objects.get(slug=category_name_slug)
        except Category.DoesNotExist:
            return None

    def get(self, request, category_name_slug):
        category = self.get_category(category_name_slug)

        if category is None:
            return redirect(reverse('rango:index'))

        form = PageForm()

        return render(request, 'rango/add_page.html', {
            'form': form, 
            'category': category
        })

    def post(self, request, category_name_slug):

        category = self.get_category(category_name_slug)
        if category is None:
            return redirect(reverse('rango:index'))
        
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()

            return redirect(
                reverse('rango:show_category', 
                        kwargs={'category_name_slug': category_name_slug})
            )
        else:
                print(form.errors)

        return render(request, 'rango/add_page.html', {
            'form': form,
            'category': category
        })

class RegisterView(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'registration/registration_form.html', {'form': form})
    
    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'registration/registration_form.html', {'form': form})



class RestrictedView(View):
    def get(self, request):
        return render(request, 'rango/restricted.html')

# A helper method


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookies_handler(request, response):
    # Get the number of visits to the site.
    # We use the COOKIES.get() function to obtain the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(request.session.get('visits', '1'))

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


class GotoURLView(View):
    def get(self, request):

        url = '/rango/'

        page_id = request.GET['page_id']

        if page_id:
            try:
                page = Page.objects.get(id=page_id)
                page.views += 1
                page.save()
                url = page.url
            except Page.DoesNotExist:
                pass

        return redirect(url)

class RegisterProfileView(View):
    def get(self, request):
        form = UserProfileForm()
        return render(request, 'registration/profile_registration.html', {'form': form})

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('index')
        else:
            print(form.errors)

        return render(request, 'registration/profile_registration.html', {'form': form})
    



class ProfileView(View):
    def get_user_details(self, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        user_profile = UserProfile.objects.get_or_create(user=user)[0]
        form = UserProfileForm({'website': user_profile.website,
                                'picture': user_profile.picture})

        return (user, user_profile, form)
    
    @method_decorator(login_required)
    def get(self, request, username):
        try: 
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        
        # SECURITY CHECK
        if request.user != user:
            return redirect('rango:index')
        
        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        
        return render(request, 'rango/profile.html', context=context_dict)
    
    @method_decorator(login_required)
    def post(self, request, username):
        try: 
            (user, user_profile, form) = self.get_user_details(username)
        except TypeError:
            return redirect(reverse('rango:index'))
        
        #SECURITY CHECK
        if request.user != user:
            return redirect('rango:index')
        
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:profile', user.username)
        else:
            print(form.errors)

        context_dict = {'user_profile': user_profile,
                        'selected_user': user,
                        'form': form}
        
        return render(request, 'rango/profile.html', context=context_dict)



class UsersView(View):
    def get(self, request):

        user_list = User.objects.all()

        print("DEBUG USERS:", user_list)
        return render(
            request, 
            'rango/users.html', 
            {'users': user_list}
        )
       


class AboutView(View):
    def get(self, request):

        context_dict = {
            'visits': int(request.session.get('visits', '1'))
        }

        reponse = render(
            request, 
            'rango/about.html', 
            context=context_dict
        )

        response = visitor_cookies_handler(request, reponse)
    
        return response



class AddCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = CategoryForm()

        return render(request, 'rango/add_category.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect('/rango/')
        else:
            print(form.errors)

        return render(request, 'rango/add_category.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class ListProfilesView(View):
        def get(self, request):
            profiles = UserProfile.objects.all()
            return render(request,
                          'rango/list_profiles.html',
                          {'user_profile_list': profiles}
            )


class LikeCategoryView(View):
    @method_decorator(login_required)
    def get(self, request):
        category_id = request.GET['category_id']
        try:
          category = Category.objects.get(id=int(category_id))
        except Category.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)
        category.likes += 1
        category.save()
        return HttpResponse(category.likes)

def get_category_list(max_results=0, starts_with=''):
    category_list = []

    if starts_with:
        category_list = Category.objects.filter(name__istartswith=starts_with)

    if max_results > 0:
        if len(category_list) > max_results:
            category_list = category_list[:max_results]

    return category_list

class CategorySuggestionView(View):
    def get(self, request):
        if 'suggestion' in request.GET:
            suggestion = request.GET['suggestion']
        else:
            suggestion = ''

        category_list = get_category_list(
                max_results=8,
                starts_with=suggestion)
        
        if len(category_list) == 0:
            category_list = Category.objects.order_by('-likes')

        return render(request,
                      'rango/category_list.html',
                      {'categories': category_list})