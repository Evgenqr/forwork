from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.Home, name="home"),
    path('fas/', views.Fas, name="fas"),
    # -----> For User
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name="loginuser"),
    #  <---- End For User
    # -----> Category
    path('category/create', views.createcategory, name='createcategory'),
    path('category/<str:slug>/view/', views.viewcategory, name='viewcategory'),
    path('category/<str:slug>/delete',
         views.deletecategory,
         name='deletecategory'),
    #  <---- End Category
    # -----> Document
    path('document/<str:slug>/',
         views.DocumentView.as_view(),
         name='document'),
    path('create/', views.createdocument, name='createdocument'),
    # path('create/',
    #      views.FileFieldView.as_view(),
    #      name='createdocument'),
    path('document/<str:slug>/view/', views.viewdocument, name='viewdocument'),
    path('document/<str:slug>/delete',
         views.deletecategory,
         name='deletedocument'),

    #  <---- End Document
    # path('search/', views.SearchView.as_view(), name='search'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
