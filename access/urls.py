from django.urls import path
from .views import ResendAccessView

urlpatterns = [
    path("resend-access/", ResendAccessView.as_view()),
]
