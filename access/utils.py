import secrets
import string


def generate_product_password(product_name: str, customer_name: str):

    product_part = product_name.split()[0][:6].upper()
    name_part = customer_name.split()[0][:6].upper()

    random_part = ''.join(
        secrets.choice(string.ascii_uppercase + string.digits)
        for _ in range(4)
    )

    return f"{product_part}-{name_part}-{random_part}"
