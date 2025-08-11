"""
URL configuration for blog_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from users import views as user_views
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from private_messages import views as message_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('private_messages/', include('private_messages.urls')),

    # User authentication flows - all centralized in your custom 'users' app views
    path('register/', user_views.register, name='register'),
    path('login/', user_views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'), name='password_reset_complete'),

    path('profile/', user_views.profile, name='profile'),
    path('profile/<str:username>/', user_views.public_profile, name='public_profile'),

    # Include all allauth social authentication URLs
    

    # Redirects for allauth routes
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=False)),
    path('accounts/signup/', RedirectView.as_view(url='/register/', permanent=False)),
    
    path('accounts/password/reset/', RedirectView.as_view(url='/password-reset/', permanent=False)),
    path('accounts/password/reset/done/', RedirectView.as_view(url='/password-reset/done/', permanent=False)),
    path('accounts/password/reset/confirm/<uidb64>/<token>/', RedirectView.as_view(url='/password-reset-confirm/<uidb64>/<token>/', permanent=False)),
    path('accounts/password/reset/complete/', RedirectView.as_view(url='/password-reset-complete/', permanent=False)),
    path('accounts/', include('allauth.urls'))

]

# Serve static files while in debug mode (for development)
# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    