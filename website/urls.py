from django.urls import path
from . import views


from .views import leaderboard_api


from . import views





from .views import profile_view

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my-profile/', profile_view, name='my-profile'),
    path('join-tournament/', views.join_tournament, name='join_tournament'),
    path('api/leaderboard/', leaderboard_api, name='leaderboard_api'),
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    # ... other URLs
]
