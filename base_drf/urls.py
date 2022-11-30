from django.urls import path, include, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('documents/', views.DocumentAPIList.as_view()),
    path('documents/<int:pk>/', views.DocumentDetailView.as_view()),
    path('documents/<int:pk>/delete/', views.DocumentAPIDestroy.as_view()),
    path('auth-djoser/', include('djoser.urls')),
    re_path('auth-djoser/', include('djoser.urls.authtoken')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
