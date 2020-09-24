from django.urls import path
from .views import (SignUpFormView, LoginFormView,
                    HistoryPageView, HomePageView,
                    AboutPageView, LogoutView)


urlpatterns = [
    path('', AboutPageView.as_view(), name='about'),
    path('signup/', SignUpFormView.as_view(), name='signup'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('history/', HistoryPageView.as_view(), name='history'),
    path('home/', HomePageView.as_view(), name='home'),
]

