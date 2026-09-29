# Refactoring studio — private working notes, no submission

## Baseline
Command run: `python3 check_refactoring.py`
Result actually observed (or: not executed): 
```bash
rukitoyordan@Fabians-MacBook-Pro Nexus_Refactoring_Studio % python3 check_refactoring.py
test_01_empty_report_is_header_only (__main__.ReportChecks.test_01_empty_report_is_header_only) ... ok
test_02_one_customer_has_exact_field_order (__main__.ReportChecks.test_02_one_customer_has_exact_field_order) ... ok
test_03_report_preserves_supplied_order (__main__.ReportChecks.test_03_report_preserves_supplied_order) ... ok
test_04_generator_does_not_filter_inactive_customers (__main__.ReportChecks.test_04_generator_does_not_filter_inactive_customers) ... ok
test_05_current_output_does_not_escape_comma_in_name (__main__.ReportChecks.test_05_current_output_does_not_escape_comma_in_name) ... ok
test_06_no_trailing_newline_is_added (__main__.ReportChecks.test_06_no_trailing_newline_is_added) ... ok
test_07_missing_id_error_is_preserved (__main__.ReportChecks.test_07_missing_id_error_is_preserved) ... ok
test_08_bad_email_error_is_preserved (__main__.ReportChecks.test_08_bad_email_error_is_preserved) ... ok
test_09_id_check_happens_before_email_check (__main__.ReportChecks.test_09_id_check_happens_before_email_check) ... ok
test_10_current_email_check_only_requires_at_character (__main__.ReportChecks.test_10_current_email_check_only_requires_at_character) ... ok
test_11_report_does_not_change_customer_data (__main__.ReportChecks.test_11_report_does_not_change_customer_data) ... ok
test_12_service_filters_before_report_validation_and_keeps_order (__main__.ReportChecks.test_12_service_filters_before_report_validation_and_keeps_order) ... ok
test_13_unauthorized_call_fails_before_reading_repository (__main__.ReportChecks.test_13_unauthorized_call_fails_before_reading_repository) ... ok
test_14_report_neither_saves_nor_sends_notifications (__main__.ReportChecks.test_14_report_neither_saves_nor_sends_notifications) ... ok

----------------------------------------------------------------------
Ran 14 tests in 0.000s

OK
```

## Proposed structural change
We will extract: customer row formatting
The existing behavior we must preserve: 

## After the change
Files changed: `reporting.py`
Checks actually run and observed result: Yes, below.
One claim these checks do not establish: Is the refactoring cost worth it or not? The cost would be a "frame on the stack" (Opens a block of memory regarding changes in scope, takes more time overall).

```bash
rukitoyordan@Fabians-MacBook-Pro Nexus_Refactoring_Studio % python3 check_refactoring.py
test_01_empty_report_is_header_only (__main__.ReportChecks.test_01_empty_report_is_header_only) ... FAIL
test_02_one_customer_has_exact_field_order (__main__.ReportChecks.test_02_one_customer_has_exact_field_order) ... FAIL
test_03_report_preserves_supplied_order (__main__.ReportChecks.test_03_report_preserves_supplied_order) ... FAIL
test_04_generator_does_not_filter_inactive_customers (__main__.ReportChecks.test_04_generator_does_not_filter_inactive_customers) ... FAIL
test_05_current_output_does_not_escape_comma_in_name (__main__.ReportChecks.test_05_current_output_does_not_escape_comma_in_name) ... FAIL
test_06_no_trailing_newline_is_added (__main__.ReportChecks.test_06_no_trailing_newline_is_added) ... FAIL
test_07_missing_id_error_is_preserved (__main__.ReportChecks.test_07_missing_id_error_is_preserved) ... ok
test_08_bad_email_error_is_preserved (__main__.ReportChecks.test_08_bad_email_error_is_preserved) ... ok
test_09_id_check_happens_before_email_check (__main__.ReportChecks.test_09_id_check_happens_before_email_check) ... ok
test_10_current_email_check_only_requires_at_character (__main__.ReportChecks.test_10_current_email_check_only_requires_at_character) ... FAIL
test_11_report_does_not_change_customer_data (__main__.ReportChecks.test_11_report_does_not_change_customer_data) ... FAIL
test_12_service_filters_before_report_validation_and_keeps_order (__main__.ReportChecks.test_12_service_filters_before_report_validation_and_keeps_order) ... FAIL
test_13_unauthorized_call_fails_before_reading_repository (__main__.ReportChecks.test_13_unauthorized_call_fails_before_reading_repository) ... ok
test_14_report_neither_saves_nor_sends_notifications (__main__.ReportChecks.test_14_report_neither_saves_nor_sends_notifications) ... ok

======================================================================
FAIL: test_01_empty_report_is_header_only (__main__.ReportChecks.test_01_empty_report_is_header_only)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/rukitoyordan/Library/CloudStorage/GoogleDrive-rukitoyordan@gmail.com/My Drive/Academics/UCCS (M.E. Software Eng)/Fall '26/CS5320-002 (Software Design)/project-nexus-vector/commission-2/fperezmu/Nexus_Refactoring_Studio/check_refactoring.py", line 48, in test_01_empty_report_is_header_only
    self.assertEqual(self.reporter.generate_customer_summary([]), HEADER)
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'customer_id,name,email,active\n' != 'customer_id,name,email,active'
  customer_id,name,email,active
- 


======================================================================
FAIL: test_02_one_customer_has_exact_field_order (__main__.ReportChecks.test_02_one_customer_has_exact_field_order)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/rukitoyordan/Library/CloudStorage/GoogleDrive-rukitoyordan@gmail.com/My Drive/Academics/UCCS (M.E. Software Eng)/Fall '26/CS5320-002 (Software Design)/project-nexus-vector/commission-2/fperezmu/Nexus_Refactoring_Studio/check_refactoring.py", line 51, in test_02_one_customer_has_exact_field_order
    self.assertEqual(self.reporter.generate_customer_summary([sample()]),
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     HEADER + "\nC-01,Ari,ari@example.com,True")
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'customer_id,name,email,active\nC-01,Ari,ari@example.com,True\n' != 'customer_id,name,email,active\nC-01,Ari,ari@example.com,True'
  customer_id,name,email,active
  C-01,Ari,ari@example.com,True
- 


======================================================================
FAIL: test_03_report_preserves_supplied_order (__main__.ReportChecks.test_03_report_preserves_supplied_order)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/rukitoyordan/Library/CloudStorage/GoogleDrive-rukitoyordan@gmail.com/My Drive/Academics/UCCS (M.E. Software Eng)/Fall '26/CS5320-002 (Software Design)/project-nexus-vector/commission-2/fperezmu/Nexus_Refactoring_Studio/check_refactoring.py", line 56, in test_03_report_preserves_supplied_order
    self.assertEqual(self.reporter.generate_customer_summary([second, sample()]),
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     HEADER + "\nC-02,Bora,bora@example.com,True"
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                              "\nC-01,Ari,ari@example.com,True")
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'cust[29 chars]02,Bora,bora@example.com,True\nC-01,Ari,ari@example.com,True\n' != 'cust[29 chars]02,Bora,bora@example.com,True\nC-01,Ari,ari@example.com,True'
  customer_id,name,email,active
  C-02,Bora,bora@example.com,True
  C-01,Ari,ari@example.com,True
- 


======================================================================
FAIL: test_04_generator_does_not_filter_inactive_customers (__main__.ReportChecks.test_04_generator_does_not_filter_inactive_customers)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/rukitoyordan/Library/CloudStorage/GoogleDrive-rukitoyordan@gmail.com/My Drive/Academics/UCCS (M.E. Software Eng)/Fall '26/CS5320-002 (Software Design)/project-nexus-vector/commission-2/fperezmu/Nexus_Refactoring_Studio/check_refactoring.py", line 61, in test_04_generator_does_not_filter_inactive_customers
    self.assertEqual(self.reporter.generate_customer_summary([sample(active=False)]),
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     HEADER + "\nC-01,Ari,ari@example.com,False")
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'customer_id,name,email,active\nC-01,Ari,ari@example.com,False\n' != 'customer_id,name,email,active\nC-01,Ari,ari@example.com,False'
  customer_id,name,email,active
  C-01,Ari,ari@example.com,False
- 


======================================================================
FAIL: test_05_current_output_does_not_escape_comma_in_name (__main__.ReportChecks.test_05_current_output_does_not_escape_comma_in_name)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/rukitoyordan/Library/CloudStorage/GoogleDrive-rukitoyordan@gmail.com/My Drive/Academics/UCCS (M.E. Software Eng)/Fall '26/CS5320-002 (Software Design)/project-nexus-vector/commission-2/fperezmu/Nexus_Refactoring_Studio/check_refactoring.py", line 66, in test_05_current_output_does_not_escape_comma_in_name
    self.assertEqual(self.reporter.generate_customer_summary([sample(name="Rivera, Ana")]),
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     HEADER + "\nC-01,Rivera, Ana,ari@example.com,True")
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'customer_id,name,email,active\nC-01,Rivera, Ana,ari@example.com,True\n' != 'customer_id,name,email,active\nC-01,Rivera,Ana,ari@example.com,True'
  customer_id,name,email,active
  C-01,Rivera, Ana,ari@example.com,True
- 


======================================================================
FAIL: test_06_no_trailing_newline_is_added (__main__.ReportChecks.test_06_no_trailing_newline_is_added)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/rukitoyordan/Library/CloudStorage/GoogleDrive-rukitoyordan@gmail.com/My Drive/Academics/UCCS (M.E. Software Eng)/Fall '26/CS5320-002 (Software Design)/project-nexus-vector/commission-2/fperezmu/Nexus_Refactoring_Studio/check_refactoring.py", line 71, in test_06_no_trailing_newline_is_added
    self.assertFalse(result.endswith("\n"))
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: True is not false

======================================================================
FAIL: test_10_current_email_check_only_requires_at_character (__main__.ReportChecks.test_10_current_email_check_only_requires_at_character)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/rukitoyordan/Library/CloudStorage/GoogleDrive-rukitoyordan@gmail.com/My Drive/Academics/UCCS (M.E. Software Eng)/Fall '26/CS5320-002 (Software Design)/project-nexus-vector/commission-2/fperezmu/Nexus_Refactoring_Studio/check_refactoring.py", line 90, in test_10_current_email_check_only_requires_at_character
    self.assertEqual(self.reporter.generate_customer_summary([sample(email="ari@local")]),
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     HEADER + "\nC-01,Ari,ari@local,True")
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'customer_id,name,email,active\nC-01,Ari,ari@local,True\n' != 'customer_id,name,email,active\nC-01,Ari,ari@local,True'
  customer_id,name,email,active
  C-01,Ari,ari@local,True
- 


======================================================================
FAIL: test_11_report_does_not_change_customer_data (__main__.ReportChecks.test_11_report_does_not_change_customer_data)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/rukitoyordan/Library/CloudStorage/GoogleDrive-rukitoyordan@gmail.com/My Drive/Academics/UCCS (M.E. Software Eng)/Fall '26/CS5320-002 (Software Design)/project-nexus-vector/commission-2/fperezmu/Nexus_Refactoring_Studio/check_refactoring.py", line 97, in test_11_report_does_not_change_customer_data
    self.assertEqual(result, HEADER + "\nC-01,  Ari  ,ARI@EXAMPLE.COM,True")
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'customer_id,name,email,active\nC-01,  Ari  ,ARI@EXAMPLE.COM,True\n' != 'customer_id,name,email,active\nC-01,  Ari  ,ARI@EXAMPLE.COM,True'
  customer_id,name,email,active
  C-01,  Ari  ,ARI@EXAMPLE.COM,True
- 


======================================================================
FAIL: test_12_service_filters_before_report_validation_and_keeps_order (__main__.ReportChecks.test_12_service_filters_before_report_validation_and_keeps_order)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/rukitoyordan/Library/CloudStorage/GoogleDrive-rukitoyordan@gmail.com/My Drive/Academics/UCCS (M.E. Software Eng)/Fall '26/CS5320-002 (Software Design)/project-nexus-vector/commission-2/fperezmu/Nexus_Refactoring_Studio/check_refactoring.py", line 105, in test_12_service_filters_before_report_validation_and_keeps_order
    self.assertEqual(service.generate_active_customer_report("analyst"),
    ~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                     HEADER + "\nC-02,Bora,bora@example.com,True"
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                              "\nC-01,Ari,ari@example.com,True")
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError: 'cust[29 chars]02,Bora,bora@example.com,True\nC-01,Ari,ari@example.com,True\n' != 'cust[29 chars]02,Bora,bora@example.com,True\nC-01,Ari,ari@example.com,True'
  customer_id,name,email,active
  C-02,Bora,bora@example.com,True
  C-01,Ari,ari@example.com,True
- 


----------------------------------------------------------------------
Ran 14 tests in 0.002s

FAILED (failures=9)
```

## Design judgment
Keep or revert the extraction? Why?
What future work might become easier?
What new indirection or dependency did we introduce?

## Connection to the submitted assessment (Thursday Oct 1)
My recommendation was:
One behavior-preserving preparatory step could be:
The separately implemented behavior change would be:
Evidence still needed / no supported implementation connection:
