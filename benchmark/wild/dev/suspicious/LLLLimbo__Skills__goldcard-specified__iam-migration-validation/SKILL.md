---
name: iam-migration-validation
description: Automated post-migration validation for iam-migration (ETBC to IAM). Use when designing or executing verification that legacy ETBC users can log in to the portal, permissions are consistent, and app/menu mappings are correct across iam-management-service, iam-auth-center-service, APISIX, and portal-front.
---

# IAM Migration Validation

## Overview

Provide a repeatable workflow to validate ETBC to IAM migration outcomes: login compatibility, permission parity, and app/menu tree mapping correctness. Use this skill to design checks, automate validation, and generate a release gate report.

## Required Inputs

Collect these before running the workflow:

- Environment name and service endpoints (IAM management, IAM auth center, portal, APISIX)
- Read-only access to ETBC and IAM databases (or an export)
- Portal login URL and target tenant(s)
- Tenant IDs in scope (run the workflow per tenant)
- Sample users list with expected roles/permissions (include edge cases)
- List of protected APIs to validate authorization behavior

## Workflow

### 1) Establish scope and sources

- Confirm repo locations and branches for `iam-migration`, `iam-management-service`, `iam-auth-center-service`, and `portal-front`.
- Use `FIELD_MAPPING_CN.md` and `src/main/resources/sql/reader/*.sql` in `iam-migration` as the mapping source of truth.
- Define pass/fail thresholds (e.g., zero login failures, zero menu diffs for sampled users).
- If migration is per-tenant, run the workflow per tenant and pass `--tenant-id` to scripts.

### 2) Build the ETBC baseline dataset

- Extract ETBC users, roles, permissions, and resource tree using the reader SQL.
- Normalize into a single dataset keyed by tenant, user, role, and resource identifiers.
- Persist as CSV/JSON for diffing and auditability.

### 3) Validate IAM data integrity

- Check legacy mapping tables for coverage and duplicates:
  `legacy_user_mapping`, `legacy_role_mapping`, `legacy_resource_mapping`, `legacy_org_mapping`.
- Validate relationship integrity:
  `iam_user_role`, `iam_role_permission`, `iam_feature_permission`, `iam_solution_layout`.
- Compare IAM menu tree to ETBC tree via legacy mappings (parent/child, order, visibility).

### 4) Validate authentication compatibility

- Test login using `iam-auth-center-service` for each password algorithm in scope.
- Confirm session data and user identity via `iam-management-service` portal endpoints.
- Include negative tests (disabled/locked users, expired credentials).

### 5) Validate authorization and menu mapping

- Fetch app/menu/permission lists from portal-facing IAM endpoints.
- Map IAM resource IDs back to ETBC via `legacy_resource_mapping`.
- Diff against the ETBC baseline; flag missing/extra permissions and menu nodes.

### 6) Run end-to-end portal checks

- Automate portal login and menu rendering (Playwright/Selenium).
- Validate that key routes are accessible and reflect expected permissions.

### 7) Report and gate

- Produce a diff report with coverage metrics and failure details.
- Enforce release gates based on thresholds and business criticality.

## Scripts

Use the scripts in `scripts/` to automate validation steps.

### validate_legacy_mappings.py

Run to validate legacy mapping coverage, duplicates, and orphans.

Example:

```
python3 scripts/validate_legacy_mappings.py \
  --etbc-users etbc_users.csv \
  --etbc-roles etbc_roles.csv \
  --etbc-resources etbc_resources.csv \
  --etbc-orgs etbc_orgs.csv \
  --legacy-user legacy_user_mapping.csv \
  --legacy-role legacy_role_mapping.csv \
  --legacy-resource legacy_resource_mapping.csv \
  --legacy-org legacy_org_mapping.csv \
  --out-dir out/mapping \
  --tenant-id 1001
```

### compare_menu_tree.py

Run to compare ETBC menu tree with IAM resources via legacy mappings. Use `--ignore-name` or `--ignore-uri` when localization differs.

Example:

```
python3 scripts/compare_menu_tree.py \
  --etbc-resources etbc_resources.csv \
  --iam-resources iam_resources.csv \
  --legacy-resource legacy_resource_mapping.csv \
  --out-dir out/menu \
  --tenant-id 1001
```

### compare_role_permissions.py

Run to compare ETBC role-resource relations with IAM role-permission assignments.

Example:

```
python3 scripts/compare_role_permissions.py \
  --etbc-role-resource etbc_role_resource.csv \
  --legacy-role legacy_role_mapping.csv \
  --legacy-resource legacy_resource_mapping.csv \
  --iam-role-permission iam_role_permission.csv \
  --out-dir out/permissions \
  --tenant-id 1001
```

### portal_login_smoke.py

Run to validate login and portal access via auth center and portal APIs. This script uses `openssl` for RSA encryption.
Set `portal_headers` in the config if the portal requires tenant-specific headers (for example `X-Iam-Tenant`).

Example:

```
python3 scripts/portal_login_smoke.py \
  --config references/portal-login-config.json \
  --out-dir out/login
```

Use `--self-test` to validate RSA encryption without calling remote endpoints.

## References

- Use `references/validation-checklist.md` for detailed checks, example query shapes, and report fields.
- Use `references/portal-login-config.json` as the config template for portal login checks.
