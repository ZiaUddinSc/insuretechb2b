import uuid

def generate_employee_code():
    """
    Generate unique Salesman / Employee Code
    Example: SM-8F3A91C2
    """
    return f"SM-{str(uuid.uuid4())[:8].upper()}"