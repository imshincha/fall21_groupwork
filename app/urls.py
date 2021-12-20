from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'app'
urlpatterns = [
    path('', views.index, name='index'),
    path('users/<int:pk>/', views.users_detail, name='users_detail'),
    path('papers/new/', views.papers_new, name='papers_new'),
    path('papers/<int:pk>/', views.papers_detail, name='papers_detail'),
    path('papers/<int:pk>/delete/', views.papers_delete, name='papers_delete'),
    path('papers/<str:category>/', views.papers_category, name='papers_category'),
    path('signup/', views.signup, name='signup'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='app/login.html'),
        name='login',
        ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]