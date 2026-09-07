import uuid

from .auth import Actor, AuthorizationService
from .events import DomainEvent, EventBus
from .errors import CustomerNotFoundError
from .models import Customer, CustomerTier
from .policies import CustomerValidationPolicy
from .repository import CustomerRepository


class CustomerRegistrationService:
    """A comparatively clean service introduced in a newer module."""

    def __init__(
        self,
        repository: CustomerRepository,
        authorization: AuthorizationService,
        validation: CustomerValidationPolicy,
        events: EventBus,
    ) -> None:
        self._repository = repository
        self._authorization = authorization
        self._validation = validation
        self._events = events

    def register(
        self,
        actor: Actor,
        name: str,
        email: str,
        tier: CustomerTier = CustomerTier.STANDARD,
    ) -> Customer:
        self._authorization.require_customer_management(actor)
        clean_name = self._validation.validate_name(name)
        clean_email = self._validation.validate_email(email)

        customer = Customer(
            customer_id=str(uuid.uuid4()),
            name=clean_name,
            email=clean_email,
            tier=tier,
        )
        self._repository.save(customer)
        self._events.publish(
            DomainEvent(
                event_type="customer.created",
                customer_id=customer.customer_id,
                payload={"name": customer.name, "email": customer.email},
            )
        )
        return customer


class CustomerLifecycleService:
    def __init__(
        self,
        repository: CustomerRepository,
        authorization: AuthorizationService,
        events: EventBus,
    ) -> None:
        self._repository = repository
        self._authorization = authorization
        self._events = events

    def deactivate(self, actor: Actor, customer_id: str, reason: str) -> Customer:
        self._authorization.require_customer_management(actor)
        customer = self._repository.get(customer_id)
        if customer is None:
            raise CustomerNotFoundError(customer_id)

        if len(reason.strip()) < 5:
            raise ValueError("deactivation reason must contain at least five characters")

        customer.active = False
        self._repository.save(customer)
        self._events.publish(
            DomainEvent(
                event_type="customer.deactivated",
                customer_id=customer.customer_id,
                payload={"email": customer.email, "reason": reason.strip()},
            )
        )
        return customer
