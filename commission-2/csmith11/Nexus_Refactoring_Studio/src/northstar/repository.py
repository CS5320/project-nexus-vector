from .models import Customer

class CustomerRepository:
    def __init__(self) -> None:
        self._customers: dict[str, Customer] = {}

    def save(self, customer: Customer) -> None:
        self._customers[customer.customer_id] = customer

    def get(self, customer_id: str) -> Customer | None:
        return self._customers.get(customer_id)

    def all(self) -> list[Customer]:
        return list(self._customers.values())
