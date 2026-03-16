import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY


def send_order_confirmation(email, customer_name, product_name, password, access_url):

    subject = "Seu acesso ao produto"

    html_content = f"""
    <h1>Olá {customer_name}</h1>

    <p>Obrigado pela compra do produto:</p>
    <strong>{product_name}</strong>

    <p>Use os dados abaixo para acessar:</p>

    <p>Email: {email}</p>
    <p>Senha: {password}</p>

    <p>Acesse aqui:</p>
    <a href="{access_url}">Abrir área do produto</a>
    """

    resend.Emails.send({
        # "from": "Universo Educativo <onboarding@resend.dev>",
        "from": "onboarding@resend.dev",
        "to": email,
        "subject": subject,
        "html": html_content,
    })
