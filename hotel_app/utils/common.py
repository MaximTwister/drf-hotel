from django.db.models import Q

from hotel_app.models import Booking, Room


def find_room(persons, booking_start, booking_end, hotel):
    booked_rooms_ids = set(
        Booking.objects.filter(
            Q(booking_start__range=[booking_start, booking_end]) |
            Q(booking_end__range=[booking_start, booking_end])
        ).values_list("room", flat=True)
    )
    booked_rooms = Room.objects.filter(id__in=booked_rooms_ids)
    print(f"Hotel Bookings: {booked_rooms}")

    suitable_rooms = set(hotel.rooms.filter(beds=persons))
    available_rooms = suitable_rooms.difference(booked_rooms)
    print(f"Available Rooms: {available_rooms}")
    return available_rooms.pop()

