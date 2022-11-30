from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.DocumentListView.as_view(), name="home"),
    #  -----> Search
    path('search/', views.SearchView.as_view(), name='search'),
    path('ext_search/', views.ExtSearch.as_view(), name='ext_search'),

    #  <---- End Search

    # -----> For User
    # path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    # path('login/', views.LoginView.as_view(), name="loginuser"),
    path('login_form/', views.LoginView.as_view(), name="login_form"),
    #  <---- End For User
    # -----> Category
    path('category/<str:slug>/', views.CategoryListView.as_view(),
         name='category'),
    path('departament/<str:slug>/', views.DepartamentListView.as_view(),
         name='departament'),
    path('status/<str:slug>/', views.StatusListView.as_view(), name='status'),
    #  <---- End Category
    # -----> Document
    path('document/<str:slug>/', views.DocumentDetailView.as_view(),
         name='document_detail'),
    path('create/',
         views.DocumentCreateView.as_view(),
         name='createdocument'),
    path('document/<str:slug>/view/',
         views.DocumentUpdateView.as_view(), name='viewdocument'),
    path('document/<str:slug>/delete/',
         views.DocumentDelete.as_view(), name='deletedocument'),
    #  <---- End Document
    # -----> Law
    path('laws/<str:slug>/', views.LawListView.as_view(), name='law'),
    #  <---- End Law
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
