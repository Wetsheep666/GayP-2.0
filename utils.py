def format_currency(amount):
    return f"${amount:,.2f}"
import uuid

def generate_group_id():
    return str(uuid.uuid4())
