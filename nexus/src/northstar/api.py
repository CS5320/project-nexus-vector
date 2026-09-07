from .auth import Actor
from .customer_service import CustomerService
from .errors import AuthorizationError, CustomerNotFoundError, NorthstarError
from .models import CustomerTier
from .services import CustomerRegistrationService


class CustomerApi:
    def __init__(
        self,
        legacy_service: CustomerService,
        registration_service: CustomerRegistrationService,
    ) -> None:
        self.legacy_service = legacy_service
        self.registration_service = registration_service

    def create_legacy(self, payload: dict, actor_role: str) -> tuple[int, dict]:
        try:
            customer = self.legacy_service.create_customer(
                actor_role=actor_role,
                name=payload.get("name"),
                email=payload.get("email"),
                tags=payload.get("tags"),
            )
            return 201, {"customer": customer.__dict__}
        except NorthstarError as exc:
            return 400, {"error": str(exc)}
        except PermissionError:
            return 403, {"message": "forbidden"}

    def create_v2(self, payload: dict, actor: Actor) -> tuple[int, dict]:
        try:
            customer = self.registration_service.register(
                actor=actor,
                name=payload.get("name"),
                email=payload.get("email"),
                tier=CustomerTier(payload.get("tier", "standard")),
            )
            return 201, {
                "data": {
                    "id": customer.customer_id,
                    "name": customer.name,
                    "email": customer.email,
                    "tier": customer.tier.value,
                }
            }
        except AuthorizationError as exc:
            return 403, {"error": {"code": "forbidden", "message": str(exc)}}
        except NorthstarError as exc:
            return 400, {"error": {"code": "invalid_request", "message": str(exc)}}

    def update_email_legacy(
        self,
        customer_id: str,
        payload: dict,
        actor_role: str,
    ) -> tuple[int, dict]:
        try:
            customer = self.legacy_service.update_customer_email(
                actor_role,
                customer_id,
                payload.get("email"),
            )
            return 200, customer.__dict__
        except Exception as exc:
            # Legacy endpoint leaks implementation details.
            return 500, {
                "status": "failed",
                "exception": type(exc).__name__,
                "details": str(exc),
            }

    def customer_summary(
        self,
        customer_id: str,
        actor_role: str,
    ) -> tuple[int, dict]:
        try:
            summary = self.legacy_service.get_customer_contact_summary(
                actor_role,
                customer_id,
            )
            return 200, {"summary": summary}
        except CustomerNotFoundError:
            return 404, {"message": "customer not found"}
