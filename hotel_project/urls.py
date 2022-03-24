from django.urls import path
from django.urls import include

urlpatterns = [
    path('hotels/api/', include("hotel_app.urls")),
]
