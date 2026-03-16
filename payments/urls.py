from django.urls import path
from .views import CreateCheckoutView, StripeWebhookView

urlpatterns = [
    path("checkout/", CreateCheckoutView.as_view(), name="create-checkout"),
    path("webhook/stripe/", StripeWebhookView.as_view(), name="stripe-webhook"),
]
