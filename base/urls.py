from django.urls import path # type: ignore
from . import views
from django.conf.urls.static import static # type: ignore
from django.conf import settings # type: ignore


urlpatterns = [
    path('', views.DocumentListView.as_view(), name="home"),

    # -----> For User
    # path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    # path('login/', views.LoginView.as_view(), name="loginuser"),
    path('login_form/', views.LoginView.as_view(), name="login_form"),
    #  <---- End For User

    # -----> Category
    path('category/<str:slug>/', views.CategoryListView.as_view(), name='category'),
    path('departament/<str:slug>/', views.DepartamentListView.as_view(), name='departament'),
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

    # path('document/<str:slug>/delete/',
    #      views.deletedocument,
    #      name='deletedocument'),
    # path('file/delete/<int:pk>/',
    #      views.deletefile,
    #      name='deletefile'),
    # path('file/<int:pk>/delete/',
    #      views.FileDelete.as_view(),
    #      name='deletefile'),
    #  <---- End Document
    #
    # -----> Law
    path('laws/<str:slug>/', views.LawListView.as_view(), name='law'),
    #  <---- End Law

    path('search/', views.SearchView.as_view(), name='search'),

    # path('category/create', views.createcategory, name='createcategory'),
    # path('category/<str:slug>/view/', views.viewcategory, name='viewcategory'),
    # path('category/<str:slug>/delete',
    #      views.deletecategory,
    #      name='deletecategory'),
    # path('document/<str:slug>/', views.document_detail_view, name='document'),
    # path('document/<str:slug>/view/',
    # views.DocumentUpdateView.as_view(),
    # name='viewdocument'),
    # path('category/<str:slug>/', views.category_detail_view, name='category'),
    # path('fas/', views.Fas, name="fas"),
    # path('laws/<str:slug>/', views.law_detail_view, name='law'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
