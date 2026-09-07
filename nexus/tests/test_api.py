from northstar.api import CustomerApi
from northstar.auth import AuthClient
from northstar.customer_service import CustomerService
from northstar.notifications import NotificationClient
from northstar.repository import CustomerRepository
from northstar.reporting import ReportGenerator

def build_api():
    service = CustomerService(CustomerRepository(), AuthClient(), NotificationClient(), ReportGenerator())
    return CustomerApi(service)

def test_create_returns_standard_error_shape():
    api = build_api()
    status, body = api.create({"name": "A", "email": "bad"}, "admin")
    assert status == 400
    assert "error" in body

def test_update_email_returns_legacy_error_shape():
    api = build_api()
    status, body = api.update_email("missing", {"email": "new@example.com"}, "admin")
    assert status == 500
    assert body["status"] == "failed"
    assert body["exception"] == "CustomerNotFoundError"
