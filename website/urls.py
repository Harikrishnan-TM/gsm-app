from django.urls import path
from . import views


from .views import profile_view

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-profile/', profile_view, name='my-profile'),
]
