from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=True)
router.register(r'tables', views.BookingsViewset, 'tables')

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('book/', views.book, name="book"),
    path('reservations/', views.reservations, name="reservations"),
    path('menu/', views.menu, name="menu"),
    path('menu-item/<int:pk>/', views.display_menu_item, name="menu_item"),  
    path('bookings/', views.bookings, name='bookings'), 
    path('menu/items/', views.MenuItemsView.as_view(), name='menu-items'),
    path('menu/items/<str:pk>/', views.SingleMenuItemView.as_view(), name='menu-item'),
    path('login/', views.login, name='login-user'),
    path('logout/', views.logout, name='logout-user'),
    path('signup/', views.signup, name='signup-user')
] + router.urls