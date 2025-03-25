from django.contrib import admin
from django.urls import path
from home.views import movie_list, book_ticket, auth_view,my_bookings, logout_view , dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', movie_list, name='movie_list'),
    path('book/<int:movie_id>/', book_ticket, name='book_ticket'),
    path('login/', auth_view, name='login'), 
    path('logout/', logout_view, name='logout'), 
    path('signup/', auth_view, name='signup'),
    path('my-bookings/', my_bookings, name='my_bookings'),
    path('dashboard/', dashboard, name='dashboard'),
]