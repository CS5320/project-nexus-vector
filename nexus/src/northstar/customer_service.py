import re
import uuid
from .auth import AuthClient
from .errors import CustomerNotFoundError, ValidationError
from .models import Customer
from .notifications import NotificationClient
from .repository import CustomerRepository
from .reporting import ReportGenerator

class CustomerService:
    """Coordinates customer-related behavior.

    NOTE: This class has grown over several releases and now performs
    customer management, authorization, validation, notifications,
    tagging, and reporting.
    """

    def __init__(self, repository: CustomerRepository, auth_client: AuthClient,
                 notification_client: NotificationClient, report_generator: ReportGenerator) -> None:
        self.repository = repository
        self.auth_client = auth_client
        self.notification_client = notification_client
        self.report_generator = report_generator

    def create_customer(self, actor_role: str, name: str, email: str,
                        tags: list[str] | None = None) -> Customer:
        if not self.auth_client.can_manage_customers(actor_role):
            raise PermissionError("not allowed")
        if name is None or len(name.strip()) < 2:
            raise ValidationError("Customer name is required")
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email or ""):
            raise ValidationError("Customer email is invalid")
        customer = Customer(str(uuid.uuid4()), name.strip(), email.strip().lower(), tags=tags or [])
        self.repository.save(customer)
        self.notification_client.send(customer.email, f"Welcome to Atlas, {customer.name}!")
        return customer

    def update_customer_email(self, actor_role: str, customer_id: str, new_email: str) -> Customer:
        if actor_role not in ("admin", "manager"):
            raise PermissionError("Forbidden")
        customer = self.repository.get(customer_id)
        if customer is None:
            raise CustomerNotFoundError(customer_id)
        if new_email is None or "@" not in new_email or "." not in new_email:
            raise ValueError("invalid email address")
        old_email = customer.email
        customer.email = new_email.strip().lower()
        self.repository.save(customer)
        self.notification_client.send(old_email, f"Your Atlas account email was changed to {customer.email}.")
        return customer

    def deactivate_customer(self, actor_role: str, customer_id: str, reason: str) -> bool:
        if not self.auth_client.can_manage_customers(actor_role):
            return False
        customer = self.repository.get(customer_id)
        if customer is None:
            return False
        if not reason or len(reason.strip()) < 5:
            raise Exception("Reason too short")
        customer.active = False
        self.repository.save(customer)
        self.notification_client.send(customer.email, f"Your Atlas account has been deactivated: {reason.strip()}")
        return True

    def add_tag(self, actor_role: str, customer_id: str, tag: str) -> Customer:
        if not self.auth_client.can_manage_customers(actor_role):
            raise PermissionError("not allowed")
        customer = self.repository.get(customer_id)
        if not customer:
            raise KeyError(customer_id)
        cleaned = tag.strip().lower()
        if cleaned and cleaned not in customer.tags:
            customer.tags.append(cleaned)
        self.repository.save(customer)
        return customer

    def generate_active_customer_report(self, actor_role: str) -> str:
        if not self.auth_client.can_run_reports(actor_role):
            raise PermissionError("not allowed to run reports")
        active = [c for c in self.repository.all() if c.active]
        return self.report_generator.generate_customer_summary(active)
