from django.urls import path, include, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('documents/', views.DocumentAPIList.as_view()),
    path('documents/<int:pk>/', views.DocumentDetailView.as_view()),
    path('documents/<int:pk>/delete/', views.DocumentAPIDestroy.as_view()),
    path('auth-djoser/', include('djoser.urls')),
    re_path('auth-djoser/', include('djoser.urls.authtoken')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
