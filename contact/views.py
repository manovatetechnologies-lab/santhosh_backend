from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

@api_view(['POST'])
def contact_api(request):
    name = request.data.get('name')
    email = request.data.get('email')
    company = request.data.get('company', '')
    service = request.data.get('service', '')
    message = request.data.get('message')

    if not name or not email or not message:
        return Response(
            {"error": "Name, email and message are required"},
            status=400
        )

    body = f"""
New Contact Request

Name: {name}
Email: {email}
Company: {company}
Service: {service}

Message:
{message}
"""

    try:
        send_mail(
            subject="New Portfolio Contact",
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["santhoshsandy@manovate.co.in"],
            fail_silently=False,
        )
    except Exception as e:
        return Response(
            {"error": f"Email failed: {str(e)}"},
            status=500
        )

    return Response({"success": "Email sent successfully"})
