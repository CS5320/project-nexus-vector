import re
import uuid

from .auth import Actor, AuthorizationService, LegacyRoleChecks
from .errors import CustomerNotFoundError, ValidationError
from .models import Customer, CustomerTier
from .notifications import NotificationClient
from .repository import CustomerRepository
from .reporting import CsvCustomerReport, LegacyCustomerReport


class CustomerService:
    """Legacy façade over several customer capabilities.

    This class has grown over multiple releases and now performs customer
    management, authorization, validation, tagging, notifications, reporting,
    and compatibility behavior.

    Some newer services overlap with this class, creating architecture drift.
    """

    def __init__(
        self,
        repository: CustomerRepository,
        authorization: AuthorizationService,
        notification_client: NotificationClient,
    ) -> None:
        self.repository = repository
        self.authorization = authorization
        self.notification_client = notification_client
        self.legacy_report = LegacyCustomerReport()
        self.csv_report = CsvCustomerReport()

    def create_customer(
        self,
        actor_role: str,
        name: str,
        email: str,
        tags: list[str] | None = None,
    ) -> Customer:
        if not LegacyRoleChecks.can_manage(actor_role):
            raise PermissionError("not allowed")

        # Validation style A
        if name is None or len(name.strip()) < 2:
            raise ValidationError("Customer name is required")
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email or ""):
            raise ValidationError("Customer email is invalid")

        customer = Customer(
            customer_id=str(uuid.uuid4()),
            name=name.strip(),
            email=email.strip().lower(),
            tier=CustomerTier.STANDARD,
            tags=tags or [],
        )
        self.repository.save(customer)

        # Direct dependency use; newer code uses domain events instead.
        self.notification_client.send(
            customer.email,
            f"Welcome to Atlas, {customer.name}!",
        )
        return customer

    def update_customer_email(
        self,
        actor_role: str,
        customer_id: str,
        new_email: str,
    ) -> Customer:
        if actor_role not in ("admin", "manager"):
            raise PermissionError("Forbidden")

        customer = self.repository.get(customer_id)
        if customer is None:
            raise CustomerNotFoundError(customer_id)

        # Validation style B: similar rule, different exception and message.
        if new_email is None or "@" not in new_email or "." not in new_email:
            raise ValueError("invalid email address")

        old_email = customer.email
        customer.email = new_email.strip().lower()
        self.repository.save(customer)
        self.notification_client.send(
            old_email,
            f"Your Atlas account email was changed to {customer.email}.",
        )
        return customer

    def deactivate_customer(
        self,
        actor_role: str,
        customer_id: str,
        reason: str,
    ) -> bool:
        # Yet another authorization path.
        actor = Actor(user_id="legacy-api", role=actor_role)
        try:
            self.authorization.require_customer_management(actor)
        except Exception:
            return False

        customer = self.repository.get(customer_id)
        if customer is None:
            return False

        if not reason or len(reason.strip()) < 5:
            raise Exception("Reason too short")

        customer.active = False
        self.repository.save(customer)
        self.notification_client.send(
            customer.email,
            f"Your Atlas account has been deactivated: {reason.strip()}",
        )
        return True

    def add_tag(
        self,
        actor_role: str,
        customer_id: str,
        tag: str,
    ) -> Customer:
        if not LegacyRoleChecks.can_manage(actor_role):
            raise PermissionError("not allowed")

        customer = self.repository.get(customer_id)
        if not customer:
            raise KeyError(customer_id)

        cleaned = tag.strip().lower()
        if cleaned and cleaned not in customer.tags:
            customer.tags.append(cleaned)
        self.repository.save(customer)
        return customer

    def change_tier(
        self,
        actor_role: str,
        customer_id: str,
        tier: str,
    ) -> Customer:
        if actor_role != "admin":
            raise PermissionError("admin required")

        customer = self.repository.get(customer_id)
        if customer is None:
            raise CustomerNotFoundError(customer_id)

        customer.tier = CustomerTier(tier)
        self.repository.save(customer)
        return customer

    def generate_active_customer_report(
        self,
        actor_role: str,
        modern: bool = False,
    ) -> str:
        if not LegacyRoleChecks.can_export(actor_role):
            raise PermissionError("not allowed to run reports")

        customers = self.repository.all()
        if modern:
            return self.csv_report.generate([c for c in customers if c.active])
        return self.legacy_report.generate_active_customer_summary(customers)

    def get_customer_contact_summary(
        self,
        actor_role: str,
        customer_id: str,
    ) -> str:
        """Demonstrates a mild Law-of-Demeter-style smell."""
        if not LegacyRoleChecks.can_manage(actor_role):
            raise PermissionError("not allowed")

        customer = self.repository.get(customer_id)
        if customer is None:
            raise CustomerNotFoundError(customer_id)

        # Exposes formatting concerns and object internals in the service layer.
        return f"{customer.name} <{customer.email}> [{customer.tier.value}]"
