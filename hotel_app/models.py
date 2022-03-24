from django.db import models
from rest_framework.exceptions import ValidationError


class City(models.Model):
    title = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.title


class Hotel(models.Model):
    title = models.CharField(max_length=30)
    city = models.ForeignKey(
        "City",
        on_delete=models.CASCADE,
        related_name="hotels",
    )

    class Meta:
        unique_together = "title", "title"

    def get_rooms_beds(self):
        rooms_by_beds = {}
        rooms = self.rooms.all()
        for room in rooms:
            rooms_by_beds[int(room.beds)] = rooms_by_beds.setdefault(room.beds, 0) + 1
        return rooms_by_beds

    def save(self, *args, **kwargs):
        max_amount = 5
        hotels_amount = self.city.hotels.count()
        if hotels_amount > max_amount:
            raise ValidationError(f"City can include maximum {max_amount} hotels")
        else:
            print(f"{self.city} has {hotels_amount} hotels")
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.city}:{self.title}"


class Room(models.Model):
    room_number = models.IntegerField()
    beds = models.IntegerField()
    hotel = models.ForeignKey(
        "Hotel",
        on_delete=models.CASCADE,
        related_name="rooms",
    )

    class Meta:
        unique_together = "hotel", "room_number"


class Booking(models.Model):
    guest_name = models.CharField(max_length=120)
    persons = models.IntegerField()
    booking_start = models.DateField()
    booking_end = models.DateField()
    room = models.ForeignKey(
        "Room",
        on_delete=models.CASCADE,
        related_name="bookings"
    )
