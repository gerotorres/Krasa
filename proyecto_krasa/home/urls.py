from django.urls import path
from home.views import (
    home_view,  # <- Aquí cambiamos index_view por home_view
    LoginView,
    LogoutView,
    RegisterView,
)

urlpatterns = [
    path(route="", view=home_view, name='index'),  # <- Usamos home_view
    path(route="login/", view=LoginView.as_view(), name='login'),
    path(route="logout/", view=LogoutView.as_view(), name='logout'),
    path(route="register/", view=RegisterView.as_view(), name='register'),
]