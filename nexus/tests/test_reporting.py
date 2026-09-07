import pytest

from northstar.auth import Actor
from northstar.errors import ReportError
from northstar.models import Customer
from northstar.reporting import CsvCustomerReport, LegacyCustomerReport


def test_modern_csv_report_includes_tier():
    report = CsvCustomerReport().generate(
        [Customer("1", "Ava", "ava@example.com")]
    )
    assert "tier" in report
    assert "standard" in report


def test_legacy_report_skips_inactive_customers():
    report = LegacyCustomerReport().generate_active_customer_summary(
        [
            Customer("1", "Ava", "ava@example.com", active=False),
            Customer("2", "Priya", "priya@example.com", active=True),
        ]
    )
    assert "Ava" not in report
    assert "Priya" in report


def test_legacy_report_duplicates_email_validation():
    with pytest.raises(ReportError):
        LegacyCustomerReport().generate_active_customer_summary(
            [Customer("1", "Ava", "bad-email")]
        )
