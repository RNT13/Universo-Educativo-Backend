import uuid

from django.shortcuts import get_object_or_404
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from emails.services import send_order_confirmation
from products.models import Product
from orders.models import Order
from .models import Payment
from .serializers import CheckoutSerializer
from access.models import ProductAccess
from access.utils import generate_product_password

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutView(APIView):

    def post(self, request):

        product_id = request.data.get("product_id")

        if not product_id:
            return Response(
                {"error": "product_id é obrigatório"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = get_object_or_404(Product, id=product_id)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",

            line_items=[
                {
                    "price_data": {
                        "currency": "brl",
                        "product_data": {
                            "name": product.name,
                        },
                        "unit_amount": int(product.price * 100),
                    },
                    "quantity": 1,
                }
            ],

            customer_creation="always",

            metadata={
                "product_id": str(product.id),
            },

            success_url="https://universo-educativo.vercel.app/success",
            cancel_url="https://universo-educativo.vercel.app/canceled",
        )

        Payment.objects.create(
            stripe_checkout_session=checkout_session.id
        )

        return Response(
            {"checkout_url": checkout_session.url},
            status=status.HTTP_201_CREATED,
        )


class StripeWebhookView(APIView):
    permission_classes = []
    authentication_classes = []

    def post(self, request):

        payload = request.body
        sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

        try:
            event = stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET,
            )
        except Exception:
            return Response(status=400)

        if event["type"] == "checkout.session.completed":

            session = event["data"]["object"]

            payment = Payment.objects.get(
                stripe_checkout_session=session["id"]
            )

            payment.status = "succeeded"

            email = session["customer_details"]["email"]
            name = session["customer_details"]["name"]

            product = Product.objects.get(
                id=session["metadata"]["product_id"]
            )

            order = Order.objects.create(
                customer_name=name,
                email=email,
                total_price=product.price
            )

            payment.order = order
            payment.save()

            password = generate_product_password(
                product_name=product.name,
                customer_name=name
            )

            ProductAccess.objects.create(
                email=email,
                customer_name=name,
                product=product,
                password=password
            )

            send_order_confirmation(
                email=email,
                customer_name=name,
                product_name=product.name,
                password=password,
                access_url="https://universo-educativo.vercel.app/acesso"
            )

        return Response(status=200)
