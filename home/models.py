from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=100)
    producer = models.CharField(max_length=100)
    duration = models.IntegerField()  # minutes
    director = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class Ticket(models.Model):
    TICKET_TYPE = (('adult', 'Người lớn'), ('child', 'Trẻ em'))
    price = models.FloatField()
    type = models.CharField(max_length=10, choices=TICKET_TYPE)
    showtime = models.DateTimeField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.movie.title} - {self.showtime}"

class TicketHolder(models.Model):
    TICKET_TYPE = (('adult', 'Người lớn'), ('child', 'Trẻ em'))
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TICKET_TYPE)
    age = models.IntegerField()
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name