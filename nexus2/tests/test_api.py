from northstar.api import CustomerApi
from northstar.auth import Actor


def build_api(legacy_service, registration):
    return CustomerApi(legacy_service, registration)


def test_legacy_create_returns_old_error_shape(legacy_service, registration):
    api = build_api(legacy_service, registration)
    status, body = api.create_legacy(
        {"name": "A", "email": "bad"},
        actor_role="admin",
    )
    assert status == 400
    assert "error" in body


def test_v2_create_returns_consistent_data_shape(legacy_service, registration):
    api = build_api(legacy_service, registration)
    status, body = api.create_v2(
        {
            "name": "Ava Morgan",
            "email": "ava@example.com",
            "tier": "premium",
        },
        Actor("u1", "admin"),
    )
    assert status == 201
    assert body["data"]["tier"] == "premium"


def test_v2_create_returns_structured_forbidden_error(legacy_service, registration):
    api = build_api(legacy_service, registration)
    status, body = api.create_v2(
        {"name": "Ava Morgan", "email": "ava@example.com"},
        Actor("u1", "viewer"),
    )
    assert status == 403
    assert body["error"]["code"] == "forbidden"


def test_legacy_update_leaks_exception_type(legacy_service, registration):
    api = build_api(legacy_service, registration)
    status, body = api.update_email_legacy(
        "missing",
        {"email": "new@example.com"},
        actor_role="admin",
    )
    assert status == 500
    assert body["exception"] == "CustomerNotFoundError"
