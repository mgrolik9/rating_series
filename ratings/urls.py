
from django.urls import path


from ratings.views import LoginView,  MainPage, RegisterView, UserLogout, HomeView, ShowView,\
    RateView, ProfileView, DeleteView, UserProfileView, TopView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('', MainPage.as_view(), name="main-page"),
    path('register/', RegisterView.as_view(), name="register"),
    path('log_out/', UserLogout.as_view(), name="logout"),
    path('home/', HomeView.as_view(), name="home"),
    path('show/<int:show_id>/', ShowView.as_view(), name="show"),
    path('rate/<int:show_id>', RateView.as_view(), name="rate"),
    path('user_profile/<int:user_id>/', UserProfileView.as_view(), name="user-profile"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('delete/<int:show_id>', DeleteView.as_view(), name="delete"),
    path('top', TopView.as_view(), name="top")
]
