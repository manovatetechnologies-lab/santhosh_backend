from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import threading
from .zoho_mail import send_zoho_mail


def send_contact_email(name, email, company, message):
    content = f"""
Name: {name}
Email: {email}
Company: {company}

Message:
{message}
"""
    send_zoho_mail(
        subject=f"New Contact Inquiry from {name}",
        content=content,
        to_email="santhoshsandy@manovate.co.in",
    )


class ContactAPIView(APIView):
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        company = request.data.get("company")
        message = request.data.get("message")

        if not name or not email or not message:
            return Response(
                {"error": "Required fields missing"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        threading.Thread(
            target=send_contact_email,
            args=(name, email, company, message),
            daemon=True,
        ).start()

        return Response(
            {"success": True, "message": "Contact request received"},
            status=status.HTTP_201_CREATED,
        )
