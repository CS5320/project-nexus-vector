from .models import Customer

def validate_customer_for_report(customer: Customer) -> None:
    # TODO: This duplicates validation performed elsewhere.
    if not customer.customer_id.strip():
        raise ValueError("missing customer id")
    if "@" not in customer.email:
        raise ValueError("bad email")
    
def _format_customer_row(customer: Customer) -> str:
    return(f"{customer.customer_id},"
           f"{customer.name},"
           f"{customer.email},"
           f"{customer.active}")

class ReportGenerator:
    def generate_customer_summary(self, customers: list[Customer]) -> str:
        lines = ["customer_id,name,email,active"]
        for customer in customers:
            validate_customer_for_report(customer)
            lines.append(_format_customer_row(customer))
        return "\n".join(lines)
        # - Example of changing behavior
        # return "\n".join(lines) + "\n"
