

from django.contrib import admin
from django.urls import path, include


#from website.models import UserProfile





#from .views import MyProfileView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api.views import register_user  # ✅ Import the API view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # App URLs
    path('api/', include('stocks.urls')),

    # Auth API for Flutter
    path('api/signup/', register_user),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Web interface
    path('', include('website.urls')),
    #path('my-profile/', MyProfileView.as_view(), name='my-profile'),
   
]






