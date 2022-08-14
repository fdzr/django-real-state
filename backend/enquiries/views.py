from django.core.mail import send_mail

from django.conf import settings
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Enquiry


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def send_enquiries_email(request):
    data = request.data
    try:
        subject = data["subject"]
        name = data["name"]
        email = data["email"]
        message = data["message"]
        from_email = data["email"]
        recipient_list = [settings.DEFAULT_FROM_EMAIL]

        send_mail(
            subject, 
            message, 
            from_email, 
            recipient_list, 
            fail_silently=True
        )

        enquiry = Enquiry(name=name, email=email, subject=subject, message=message)
        enquiry.save()

        return Response({"success": "Your enquiry was successfully submitted"})
    
    except:
        return Response({"fail": "Your enquiry was not sent. Please try again"})