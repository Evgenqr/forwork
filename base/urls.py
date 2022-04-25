from django.urls import path
from . import views
# from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.Home, name="home"),
    path('fas/', views.Fas, name="fas"),
        # -----> For User
    path('signup/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('login/', views.loginuser, name="loginuser"),
    #  <---- End For User

    # # -----> For User
    # path('signup/', views.signupuser, name='signupuser'),
    # path('logout/', views.logoutuser, name='logoutuser'),
    # path('login/', views.loginuser, name="loginuser"),
    # #  <---- End For User
    # path('search/', views.SearchView.as_view(), name='search'),
]

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
