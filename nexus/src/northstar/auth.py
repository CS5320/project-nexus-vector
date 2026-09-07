from dataclasses import dataclass

from .errors import AuthorizationError


@dataclass(frozen=True)
class Actor:
    user_id: str
    role: str


class AuthorizationService:
    """Central policy service introduced during a prior redesign."""

    CUSTOMER_MANAGERS = {"admin", "manager"}
    REPORT_VIEWERS = {"admin", "manager", "analyst"}

    def require_customer_management(self, actor: Actor) -> None:
        if actor.role not in self.CUSTOMER_MANAGERS:
            raise AuthorizationError("actor may not manage customers")

    def require_report_access(self, actor: Actor) -> None:
        if actor.role not in self.REPORT_VIEWERS:
            raise AuthorizationError("actor may not run customer reports")


class LegacyRoleChecks:
    """Old static helpers still used by several modules.

    TODO: Decide whether these should be removed or adapted to delegate to
    AuthorizationService.
    """

    @staticmethod
    def can_manage(role: str) -> bool:
        return role in ("admin", "manager")

    @staticmethod
    def can_export(role: str) -> bool:
        return role in ("admin", "analyst", "manager")
