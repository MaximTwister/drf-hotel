from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from hotel_app.models import (
    Booking,
    Hotel,
    City,
)
from hotel_app.utils.common import find_room


class HotelSerializer(serializers.ModelSerializer):
    rooms_beds = serializers.ReadOnlyField(source="get_rooms_beds")

    class Meta:
        model = Hotel
        fields = ("title", "city", "rooms_beds")


class BookingSerializer(serializers.ModelSerializer):
    city = serializers.CharField(read_only=True)
    hotel = serializers.CharField(read_only=True)

    class Meta:
        model = Booking
        fields = ("guest_name", "booking_start", "booking_end", "city", "hotel", "persons")

    @staticmethod
    def get_hotel(city, hotel):
        try:
            city = City.objects.get(title=city)
            hotel = city.hotels.get(title=hotel)
        except ObjectDoesNotExist as e:
            raise serializers.ValidationError(
                {"error": f"{city}:{hotel} - {e}"}
            )
        print(f"Hotel Detected: {hotel}")
        return hotel

    def to_internal_value(self, data):
        print(f"Raw Booking data: {data}")
        self.hotel = self.get_hotel(data.get("city"), data.get("hotel"))
        internal_data = super().to_internal_value(data)
        print(f"Internal Booking data: {internal_data}")
        return internal_data

    def create(self, validated_data):
        print(f"Validated data: {validated_data}")
        booking_start = validated_data.pop("booking_start")
        booking_end = validated_data.pop("booking_end")
        persons = validated_data.pop("persons")
        room = find_room(persons, booking_start, booking_end, self.hotel)
        booking = Booking.objects.create(
            guest_name=validated_data.pop("guest_name"),
            persons=persons,
            booking_start=booking_start,
            booking_end=booking_end,
            room=room,
        )
        print(f"Booking Instance: {booking}")
        return booking
