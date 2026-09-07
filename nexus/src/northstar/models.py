from dataclasses import dataclass, field
from enum import Enum


class CustomerTier(str, Enum):
    STANDARD = "standard"
    PREMIUM = "premium"
    ENTERPRISE = "enterprise"


@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    active: bool = True
    tier: CustomerTier = CustomerTier.STANDARD
    tags: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CustomerSnapshot:
    customer_id: str
    name: str
    email: str
    active: bool
    tier: str
    tags: tuple[str, ...]

    @classmethod
    def from_customer(cls, customer: Customer) -> "CustomerSnapshot":
        return cls(
            customer_id=customer.customer_id,
            name=customer.name,
            email=customer.email,
            active=customer.active,
            tier=customer.tier.value,
            tags=tuple(customer.tags),
        )
