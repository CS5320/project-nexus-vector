#!/usr/bin/env python3
"""Instructor-authored characterization checks, NOT upstream Nexus tests.
Run with Python 3.10+ from this folder. No pip install or network is required.
The suite checks selected observable behavior; it is not an equivalence proof.
"""
from pathlib import Path
import sys
if sys.version_info < (3, 10):
    raise SystemExit("Use Python 3.10 or newer; the supplied source uses modern type hints.")
sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from copy import deepcopy
import unittest
from northstar.models import Customer
from northstar.reporting import ReportGenerator
from northstar.repository import CustomerRepository
from northstar.auth import AuthClient
from northstar.notifications import NotificationClient
from northstar.customer_service import CustomerService

HEADER = "customer_id,name,email,active"

def sample(**changes):
    fields = dict(customer_id="C-01", name="Ari", email="ari@example.com", active=True)
    fields.update(changes)
    return Customer(**fields)

class TrackingRepository(CustomerRepository):
    def __init__(self):
        super().__init__()
        self.reads = 0
        self.writes = 0
    def all(self):
        self.reads += 1
        return super().all()
    def save(self, customer):
        self.writes += 1
        return super().save(customer)

def make_service():
    return CustomerService(TrackingRepository(), AuthClient(),
                           NotificationClient(), ReportGenerator())

class ReportChecks(unittest.TestCase):
    def setUp(self):
        self.reporter = ReportGenerator()

    def test_01_empty_report_is_header_only(self):
        self.assertEqual(self.reporter.generate_customer_summary([]), HEADER)

    def test_02_one_customer_has_exact_field_order(self):
        self.assertEqual(self.reporter.generate_customer_summary([sample()]),
                         HEADER + "\nC-01,Ari,ari@example.com,True")

    def test_03_report_preserves_supplied_order(self):
        second = sample(customer_id="C-02", name="Bora", email="bora@example.com")
        self.assertEqual(self.reporter.generate_customer_summary([second, sample()]),
                         HEADER + "\nC-02,Bora,bora@example.com,True"
                                  "\nC-01,Ari,ari@example.com,True")

    def test_04_generator_does_not_filter_inactive_customers(self):
        self.assertEqual(self.reporter.generate_customer_summary([sample(active=False)]),
                         HEADER + "\nC-01,Ari,ari@example.com,False")

    def test_05_current_output_does_not_escape_comma_in_name(self):
        # Characterizes the existing output. It does NOT recommend this CSV policy.
        self.assertEqual(self.reporter.generate_customer_summary([sample(name="Rivera, Ana")]),
                         HEADER + "\nC-01,Rivera, Ana,ari@example.com,True")

    def test_06_no_trailing_newline_is_added(self):
        result = self.reporter.generate_customer_summary([sample()])
        self.assertFalse(result.endswith("\n"))

    def test_07_missing_id_error_is_preserved(self):
        with self.assertRaises(ValueError) as err:
            self.reporter.generate_customer_summary([sample(customer_id="  ")])
        self.assertEqual(str(err.exception), "missing customer id")

    def test_08_bad_email_error_is_preserved(self):
        with self.assertRaises(ValueError) as err:
            self.reporter.generate_customer_summary([sample(email="broken")])
        self.assertEqual(str(err.exception), "bad email")

    def test_09_id_check_happens_before_email_check(self):
        with self.assertRaises(ValueError) as err:
            self.reporter.generate_customer_summary([sample(customer_id="", email="broken")])
        self.assertEqual(str(err.exception), "missing customer id")

    def test_10_current_email_check_only_requires_at_character(self):
        # This report check is weaker than creation's email check.
        self.assertEqual(self.reporter.generate_customer_summary([sample(email="ari@local")]),
                         HEADER + "\nC-01,Ari,ari@local,True")

    def test_11_report_does_not_change_customer_data(self):
        customers = [sample(name="  Ari  ", email="ARI@EXAMPLE.COM", tags=["VIP", "vip"])]
        before = deepcopy(customers)
        result = self.reporter.generate_customer_summary(customers)
        self.assertEqual(result, HEADER + "\nC-01,  Ari  ,ARI@EXAMPLE.COM,True")
        self.assertEqual(customers, before)

    def test_12_service_filters_before_report_validation_and_keeps_order(self):
        service = make_service()
        service.repository.save(sample(customer_id="C-02", name="Bora", email="bora@example.com"))
        service.repository.save(sample(customer_id="C-X", email="broken", active=False))
        service.repository.save(sample())
        self.assertEqual(service.generate_active_customer_report("analyst"),
                         HEADER + "\nC-02,Bora,bora@example.com,True"
                                  "\nC-01,Ari,ari@example.com,True")

    def test_13_unauthorized_call_fails_before_reading_repository(self):
        service = make_service()
        with self.assertRaises(PermissionError) as err:
            service.generate_active_customer_report("viewer")
        self.assertEqual(str(err.exception), "not allowed to run reports")
        self.assertEqual(service.repository.reads, 0)

    def test_14_report_neither_saves_nor_sends_notifications(self):
        service = make_service()
        service.repository.save(sample())
        writes_before = service.repository.writes
        service.generate_active_customer_report("analyst")
        self.assertEqual(service.repository.writes, writes_before)
        self.assertEqual(service.notification_client.sent_messages, [])

if __name__ == "__main__":
    unittest.main(verbosity=2)
