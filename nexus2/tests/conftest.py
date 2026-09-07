import pytest

from northstar.auth import AuthorizationService
from northstar.customer_service import CustomerService
from northstar.events import EventBus
from northstar.notifications import (
    CustomerNotificationSubscriber,
    NotificationClient,
)
from northstar.policies import CustomerValidationPolicy
from northstar.repository import InMemoryCustomerRepository
from northstar.services import CustomerLifecycleService, CustomerRegistrationService


@pytest.fixture
def repository():
    return InMemoryCustomerRepository()


@pytest.fixture
def auth():
    return AuthorizationService()


@pytest.fixture
def notifications():
    return NotificationClient()


@pytest.fixture
def event_bus(notifications):
    bus = EventBus()
    bus.subscribe(CustomerNotificationSubscriber(notifications))
    return bus


@pytest.fixture
def validation():
    return CustomerValidationPolicy()


@pytest.fixture
def registration(repository, auth, validation, event_bus):
    return CustomerRegistrationService(repository, auth, validation, event_bus)


@pytest.fixture
def lifecycle(repository, auth, event_bus):
    return CustomerLifecycleService(repository, auth, event_bus)


@pytest.fixture
def legacy_service(repository, auth, notifications):
    return CustomerService(repository, auth, notifications)
