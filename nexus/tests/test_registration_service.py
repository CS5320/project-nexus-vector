import pytest

from northstar.auth import Actor
from northstar.errors import AuthorizationError, ValidationError
from northstar.models import CustomerTier


def test_registration_normalizes_input(registration):
    customer = registration.register(
        Actor("u1", "admin"),
        "  Ava Morgan  ",
        "AVA@EXAMPLE.COM",
    )
    assert customer.name == "Ava Morgan"
    assert customer.email == "ava@example.com"


def test_registration_publishes_notification(registration, notifications):
    customer = registration.register(
        Actor("u1", "manager"),
        "Priya Shah",
        "priya@example.com",
    )
    assert notifications.sent_messages == [
        ("priya@example.com", "Welcome to Atlas, Priya Shah!")
    ]


def test_registration_rejects_bad_email(registration):
    with pytest.raises(ValidationError):
        registration.register(
            Actor("u1", "admin"),
            "Priya Shah",
            "bad-email",
        )


def test_registration_rejects_unauthorized_actor(registration):
    with pytest.raises(AuthorizationError):
        registration.register(
            Actor("u1", "viewer"),
            "Priya Shah",
            "priya@example.com",
        )


def test_registration_preserves_tier(registration):
    customer = registration.register(
        Actor("u1", "admin"),
        "Enterprise User",
        "enterprise@example.com",
        CustomerTier.ENTERPRISE,
    )
    assert customer.tier is CustomerTier.ENTERPRISE
