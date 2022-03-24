from random import choice, randint

from django.db import IntegrityError
from rest_framework.exceptions import ValidationError

from hotel_app.models import (
    Hotel,
    City,
    Room,
)
from hotel_app.utils.constants import (
    CITIES,
    HOTELS_LETTERS,
)


def create_cities():
    cities = [City(title=city) for city in CITIES]
    try:
        City.objects.bulk_create(cities)
    except IntegrityError:
        print(f"{cities} : some of these cities already exists")


def create_hotels():
    cities = City.objects.all()
    hotels = [Hotel(title=f"Hotel_{letter}") for letter in HOTELS_LETTERS]
    for hotel in hotels:
        hotel.city = choice(cities)
        try:
            hotel.save()
            hotel_rooms_amount = randint(100, 1000)
            create_rooms(hotel, hotel_rooms_amount)
        except (IntegrityError, ValidationError) as e:
            if e is IntegrityError:
                print(f"{hotel} : already exists in the {hotel.city}")
            else:
                print(e)


def create_rooms(hotel, hotel_rooms_amount):
    print(f"Create {hotel_rooms_amount} rooms for {hotel}\n")
    rooms = []
    for num in range(1, hotel_rooms_amount):
        room = Room(
            hotel=hotel,
            room_number=num,
            beds=randint(1, 4),
        )
        rooms.append(room)
    Room.objects.bulk_create(rooms)


def main():
    print("Create cities")
    create_cities()
    print("Create hotels")
    create_hotels()


main()
