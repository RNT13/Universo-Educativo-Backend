from rest_framework.views import APIView
from rest_framework.response import Response
from access.models import ProductAccess
from emails.services import send_order_confirmation


class ResendAccessView(APIView):

    def post(self, request):

        email = request.data.get("email")

        accesses = ProductAccess.objects.filter(email=email)

        if not accesses.exists():
            return Response({"error": "Nenhuma compra encontrada"}, status=404)

        for access in accesses:

            send_order_confirmation(
                email=access.email,
                customer_name=access.customer_name,
                product_name=access.product.name,
                password=access.password,
                access_url=access.product.file_url
            )

        return Response({"message": "Acesso reenviado"})
