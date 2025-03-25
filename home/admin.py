from django.contrib import admin
from .models import Movie, Ticket, TicketHolder

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'producer', 'duration', 'director', 'genre') 
    list_filter = ('genre',)  
    search_fields = ('title', 'director')  
    ordering = ('title',)  

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('movie', 'price', 'type', 'showtime')
    list_filter = ('type', 'showtime')
    search_fields = ('movie__title',) 
    ordering = ('showtime',)  

@admin.register(TicketHolder)
class TicketHolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'age', 'ticket') 
    list_filter = ('type',)  
    search_fields = ('name',)  
    ordering = ('name',) 