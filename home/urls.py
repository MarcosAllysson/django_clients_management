from django.urls import path
from .views import home, my_logout, Cookie


urlpatterns = [
    path('', home, name="home"),
    path('cookie/', Cookie.as_view(), name="cookie"),
    path('logout/', my_logout, name="logout"),
]
