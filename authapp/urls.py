from django.urls import path  # this is used to specify the route to uniform resorce locator to the specific views function logic
from . import views  # This is used to import all the views logics
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView   # TokenObtainPairView → Takes username + password → returns access and refresh tokens. (Login)
from .views import debug_token
# TokenRefreshView → Takes a refresh token → returns a new access token.

urlpatterns = [
    path("register/",views.register_user,name="register_user") ,   # re'ister/ is the url address,  views.Register_User is function logic name
    path("login/",TokenObtainPairView.as_view(), name ="Token_obtain_pair"),
    path("token/refresh/",TokenRefreshView.as_view(),name= "token_refresh"),
    path('debug-token/', debug_token),
]
