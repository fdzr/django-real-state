from django.urls import path
from . import views


urlpatterns = [
    path(
        "",
        views.send_enquiries_email,
        name="send-enquiry"
    ),
]