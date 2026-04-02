from django.urls import path

from .import views

urlpatterns = [
    # New account signup.
    path("register/", views.register, name="register"),
    # Email activation callback.
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    # Session login/logout.
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    # Account dashboard and profile editing.
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),

]