from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hotel_app.models import Hotel, Booking
from hotel_app.serializers import (
    HotelSerializer,
    BookingSerializer,
)


@api_view(["GET"])
def api_hotels(request):
    if request.method == "GET":
        hotels = Hotel.objects.all()
        serializer = HotelSerializer(hotels, many=True)
        return Response(serializer.data)


@api_view(["GET", "POST"])
def api_booking(request):
    if request.method == "GET":
        print(f"Request data: {request.data}")
        guest_name = request.data.get("guest_name")
        if guest_name:
            booking = Booking.objects.filter(guest_name=guest_name)
        else:
            booking = Booking.objects.all()
        serializer = BookingSerializer(booking, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(f"BookingSerializer: {serializer}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
