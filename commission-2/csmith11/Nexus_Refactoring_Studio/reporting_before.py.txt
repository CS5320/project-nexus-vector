from .models import Customer

def validate_customer_for_report(customer: Customer) -> None:
    # TODO: This duplicates validation performed elsewhere.
    if not customer.customer_id.strip():
        raise ValueError("missing customer id")
    if "@" not in customer.email:
        raise ValueError("bad email")

class ReportGenerator:
    def generate_customer_summary(self, customers: list[Customer]) -> str:
        lines = ["customer_id,name,email,active"]
        for customer in customers:
            validate_customer_for_report(customer)
            lines.append(f"{customer.customer_id},{customer.name},{customer.email},{customer.active}")
        return "\n".join(lines)
