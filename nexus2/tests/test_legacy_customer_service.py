import pytest

from northstar.errors import CustomerNotFoundError, ValidationError


def test_legacy_create_normalizes_email_and_sends_notification(legacy_service):
    customer = legacy_service.create_customer(
        actor_role="admin",
        name="Ava Morgan",
        email="AVA@EXAMPLE.COM",
    )
    assert customer.email == "ava@example.com"
    assert legacy_service.notification_client.sent_messages == [
        ("ava@example.com", "Welcome to Atlas, Ava Morgan!")
    ]


def test_legacy_create_rejects_invalid_email(legacy_service):
    with pytest.raises(ValidationError):
        legacy_service.create_customer(
            actor_role="admin",
            name="Ava Morgan",
            email="not-an-email",
        )


def test_legacy_update_email_uses_value_error(legacy_service):
    customer = legacy_service.create_customer(
        actor_role="admin",
        name="Carlos Rivera",
        email="carlos@example.com",
    )
    with pytest.raises(ValueError):
        legacy_service.update_customer_email(
            actor_role="manager",
            customer_id=customer.customer_id,
            new_email="broken",
        )


def test_legacy_deactivate_returns_false_when_missing(legacy_service):
    assert legacy_service.deactivate_customer(
        actor_role="admin",
        customer_id="missing",
        reason="Requested by customer",
    ) is False


def test_legacy_add_tag_raises_key_error_for_missing_customer(legacy_service):
    with pytest.raises(KeyError):
        legacy_service.add_tag("admin", "missing", "priority")


def test_legacy_contact_summary_exposes_formatting_concern(legacy_service):
    customer = legacy_service.create_customer(
        "admin",
        "Priya Shah",
        "priya@example.com",
    )
    summary = legacy_service.get_customer_contact_summary(
        "manager",
        customer.customer_id,
    )
    assert summary == "Priya Shah <priya@example.com> [standard]"


def test_legacy_update_missing_customer_raises_specific_error(legacy_service):
    with pytest.raises(CustomerNotFoundError):
        legacy_service.update_customer_email(
            "admin",
            "missing",
            "new@example.com",
        )
