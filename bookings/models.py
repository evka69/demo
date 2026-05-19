from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.full_name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('scheduled', 'Мероприятие назначено'),
        ('completed', 'Мероприятие завершено'),
    ]

    ROOM_CHOICES = [
        ('auditorium', 'Аудитория'),
        ('coworking', 'Коворкинг'),
        ('cinema', 'Кинозал'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Постоплата в офисе организации'),
        ('card', 'Оплата картой МИР'),
        ('transfer', 'Предоплата по QR-коду'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    room_type = models.CharField(max_length=20, choices=ROOM_CHOICES)
    conference_date = models.DateTimeField()
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    review = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.room_type}"



