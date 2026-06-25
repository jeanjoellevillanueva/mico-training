from django.urls import path, include
from rango import views
from rango.views import AboutView

app_name = 'rango'

app_name = 'rango'

urlpatterns = [

    # 🏠 HOME
    path('', views.IndexView.as_view(), name='index'),

    # ℹ️ ABOUT
    path('about/', views.AboutView.as_view(), name='about'),

    # 📂 CATEGORY DETAIL
    path(
        'category/<slug:category_name_slug>/',
        views.ShowCategoryView.as_view(),
        name='show_category'
    ),

    # ➕ ADD CATEGORY
    path(
        'add_category/',
        views.AddCategoryView.as_view(),
        name='add_category'
    ),

    # ➕ ADD PAGE (inside category)
    path(
        'category/<slug:category_name_slug>/add_page/',
        views.AddPageView.as_view(),
        name='add_page'
    ),

    # 🔐 REGISTER
    path('register/', views.RegisterView.as_view(), name='register'),

    # 🚫 RESTRICTED
    path('restricted/', views.RestrictedView.as_view(), name='restricted'),

    # 🔁 GOTO URL tracking
    path('goto/', views.GotoURLView.as_view(), name='goto'),

    # 👤 PROFILE
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile'),

    path('profiles/', views.ListProfilesView.as_view(), name='list_profiles'),

    # 👥 USERS LIST
    path('users/', views.UsersView.as_view(), name='users'),

    path('like_category/', views.LikeCategoryView.as_view(), name='like_category'),

    path('suggest/', views.CategorySuggestionView.as_view(), name='suggest'),

    path('search_add_page/', views.SearchAddPageView.as_view(), name='search_add_page'),

# When adding a features Step 6 (Add URLS)
    path('save_bookmark/', views.SaveBookmarkView.as_view(), name='save_bookmark'),

    path('bookmarks/', views.MyBookmarksView.as_view(), name='bookmarks'),

    path('page/<int:page_id>/report/', views.ReportBrokenLinkView.as_view(), name='report_broken_link'),

    path('learning_notes/', views.LearningNotesView.as_view(), name='learning_notes'),

    path('learning_notes/add/', views.AddLearningNoteView.as_view(), name='add_learning_note'),

    path('learning_notes/<int:note_id>/reviewed/', views.MarkNoteReviewedView.as_view(), name='mark_note_reviewed'),

    path('ajax/load_pages/', views.LoadPagesView.as_view(), name='load_pages'),
]