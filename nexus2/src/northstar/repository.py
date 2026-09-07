from abc import ABC, abstractmethod

from .models import Customer, CustomerSnapshot


class CustomerRepository(ABC):
    @abstractmethod
    def save(self, customer: Customer) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, customer_id: str) -> Customer | None:
        raise NotImplementedError

    @abstractmethod
    def all(self) -> list[Customer]:
        raise NotImplementedError


class InMemoryCustomerRepository(CustomerRepository):
    """Simple repository with a reasonably narrow responsibility."""

    def __init__(self) -> None:
        self._customers: dict[str, Customer] = {}

    def save(self, customer: Customer) -> None:
        self._customers[customer.customer_id] = customer

    def get(self, customer_id: str) -> Customer | None:
        return self._customers.get(customer_id)

    def all(self) -> list[Customer]:
        return list(self._customers.values())

    def snapshot(self, customer_id: str) -> CustomerSnapshot | None:
        customer = self.get(customer_id)
        return CustomerSnapshot.from_customer(customer) if customer else None
