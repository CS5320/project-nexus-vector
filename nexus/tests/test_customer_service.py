import pytest
from northstar.auth import AuthClient
from northstar.customer_service import CustomerService
from northstar.errors import ValidationError
from northstar.notifications import NotificationClient
from northstar.repository import CustomerRepository
from northstar.reporting import ReportGenerator

@pytest.fixture
def service():
    return CustomerService(CustomerRepository(), AuthClient(), NotificationClient(), ReportGenerator())

def test_create_customer_normalizes_email_and_sends_notification(service):
    customer = service.create_customer("admin", "Ava Morgan", "AVA@EXAMPLE.COM")
    assert customer.email == "ava@example.com"
    assert service.notification_client.sent_messages == [("ava@example.com", "Welcome to Atlas, Ava Morgan!")]

def test_create_customer_rejects_invalid_email(service):
    with pytest.raises(ValidationError):
        service.create_customer("admin", "Ava Morgan", "not-an-email")

def test_update_email_uses_legacy_value_error(service):
    customer = service.create_customer("admin", "Carlos Rivera", "carlos@example.com")
    with pytest.raises(ValueError):
        service.update_customer_email("manager", customer.customer_id, "broken")

def test_deactivate_customer_returns_false_when_missing(service):
    assert service.deactivate_customer("admin", "missing", "Requested by customer") is False

def test_report_contains_only_active_customers(service):
    first = service.create_customer("admin", "Priya Shah", "priya@example.com")
    service.create_customer("admin", "Jordan Lee", "jordan@example.com")
    service.deactivate_customer("admin", first.customer_id, "Duplicate account")
    report = service.generate_active_customer_report("analyst")
    assert "Jordan Lee" in report
    assert "Priya Shah" not in report
