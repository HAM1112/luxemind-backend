import stripe
from django.shortcuts import redirect
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from providers.models import *
from rest_framework.decorators import permission_classes, api_view
from rest_framework import status

stripe.api_key = settings.STRIPE_KEY


class StripeCheckoutView(APIView):
    def post(self, request):
        try:
            data = request.data
            print("this is workin")

            print(data)
            # Create a PaymentIntent with the order amount and currency
            intent = stripe.PaymentIntent.create(
                amount=100,
                currency="usd",
                receipt_email="admin@admin.com",
                # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
                automatic_payment_methods={
                    "enabled": True,
                },
            )
            return Response({"intent": intent})
        except Exception as e:
            return Response(data={"error": str(e)}, status=403)


@api_view(["POST"])
def save_stripe_info(request):
    data = request.data
    course_id = data["course"]

    email = request.user.email
    name = request.user.username

    course = Course.objects.get(id=course_id)
    customer_data = stripe.Customer.list(email=email).data
    if len(customer_data) == 0:
        customer = stripe.Customer.create(
            email=email,
            name=name,
            address={
                "line1": "123 Main Street",
                "city": "Kanoor",
                "postal_code": "123232",
                "country": "DK",
            },
        )
    else:
        customer = customer_data[0]

    # price_data = stripe.Price.list(unit_amount=int(course.course_price * 100)).data
    # if len(price_data) == 0 :
    #     price = stripe.Price.create(
    #         currency='usd',
    #         unit_amount=int(course.course_price * 100),
    #         product_data={"name": "Course"}
    #     )
    # else :
    #     price = price_data[0]

    intent = stripe.PaymentIntent.create(
        customer=customer,
        currency="inr",
        shipping={
            "name": "Jenny Rosen",
            "address": {
                "line1": "510 Townsend St",
                "postal_code": "98140",
                "city": "San Francisco",
                "state": "CA",
                "country": "US",
            },
        },
        description="Software development services",
        amount=int(course.course_price * 100),
        receipt_email="admin@admin.com",
        payment_method_types=[
            "card",
        ],
    )

    # confirm_intent = stripe.PaymentIntent.confirm(intent.id)

    return Response({"clientSecret": intent["client_secret"]})
