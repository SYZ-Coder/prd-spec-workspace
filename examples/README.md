# Examples

This directory now contains executable baseline examples, not just folder conventions.

## Included Examples

- `auth-basic/`
  Login, registration, and password reset requirement sample.
- `payment-refund/`
  Payment plus refund requirement sample, including a known semantic-risk case for validation.
- `reporting-dashboard/`
  Reporting dashboard sample with custom extractor overrides.
- `approval-workflow/`
  Approval workflow sample with explicit middle states.
- `ticket-lifecycle/`
  Ticket lifecycle sample focused on trigger ownership and transition correctness.

## Structure

Each example may contain:

- `inputs/prd/`
- `inputs/notes/`
- `inputs/context/`
- `extractor-overrides.json`
- `README.md`

## Recommended Usage

1. Copy one example's `inputs/` files into the workspace `inputs/` directory.
2. Copy `extractor-overrides.json` to the workspace root when the example provides one.
3. Run `python scripts/run_pipeline.py --change-name <change-name> --domain <domain> --title "<title>"`.
4. Compare the generated DSL and validation report with the example expectation.

## Regression Role

These examples are also used by automated tests to verify:

- page extraction accuracy
- rule extraction coverage
- transition quality
- semantic validation warnings
- custom vocabulary support
