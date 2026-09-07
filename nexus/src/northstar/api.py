from .customer_service import CustomerService
from .errors import NorthstarError

class CustomerApi:
    def __init__(self, service: CustomerService) -> None:
        self.service = service

    def create(self, payload: dict, actor_role: str) -> tuple[int, dict]:
        try:
            customer = self.service.create_customer(actor_role, payload.get("name"), payload.get("email"), payload.get("tags"))
            return 201, {"customer": customer.__dict__}
        except NorthstarError as exc:
            return 400, {"error": str(exc)}
        except PermissionError:
            return 403, {"message": "forbidden"}

    def update_email(self, customer_id: str, payload: dict, actor_role: str) -> tuple[int, dict]:
        try:
            customer = self.service.update_customer_email(actor_role, customer_id, payload.get("email"))
            return 200, customer.__dict__
        except Exception as exc:
            # TODO: Legacy endpoint exposes exception type and uses a different shape.
            return 500, {"status": "failed", "exception": type(exc).__name__, "details": str(exc)}
