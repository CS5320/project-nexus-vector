from abc import ABC, abstractmethod
from csv import writer
from io import StringIO

from .errors import ReportError
from .models import Customer


class CustomerReportStrategy(ABC):
    @abstractmethod
    def generate(self, customers: list[Customer]) -> str:
        raise NotImplementedError


class CsvCustomerReport(CustomerReportStrategy):
    """Strategy implementation with a focused responsibility."""

    def generate(self, customers: list[Customer]) -> str:
        output = StringIO()
        csv_writer = writer(output)
        csv_writer.writerow(["customer_id", "name", "email", "active", "tier"])
        for customer in customers:
            csv_writer.writerow(
                [
                    customer.customer_id,
                    customer.name,
                    customer.email,
                    customer.active,
                    customer.tier.value,
                ]
            )
        return output.getvalue().strip()


class LegacyCustomerReport:
    """Older report generator preserved for compatibility.

    This class duplicates validation rules and mixes filtering, validation,
    formatting, and policy decisions.
    """

    def generate_active_customer_summary(self, customers: list[Customer]) -> str:
        lines = ["customer_id,name,email,active"]
        for customer in customers:
            if not customer.active:
                continue
            if not customer.customer_id.strip():
                raise ReportError("missing customer id")
            if "@" not in customer.email:
                raise ReportError("bad email")
            lines.append(
                f"{customer.customer_id},{customer.name},{customer.email},{customer.active}"
            )
        return "\n".join(lines)
