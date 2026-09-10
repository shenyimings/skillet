# IAM Migration Validation Checklist

## Baseline extraction (ETBC)

- Use `iam-migration` reader SQL as the canonical source.
- If migration is per-tenant, extract and validate per tenant (scope datasets by tenantId).
- Normalize into a baseline dataset keyed by: tenantId, userId/login, roleId, resourceId.
- Capture menu tree fields: resourceId, parentResourceId, sort/order, visible flag, route/path.

Suggested outputs:

- `baseline_users.csv`
- `baseline_roles.csv`
- `baseline_permissions.csv`
- `baseline_menu_tree.csv`

## IAM data integrity checks

Mapping coverage:

- `legacy_user_mapping`: all ETBC user IDs exist and map to IAM user IDs.
- `legacy_role_mapping`: all ETBC role IDs exist and map to IAM roles.
- `legacy_resource_mapping`: all ETBC resource IDs exist and map to IAM resources.
- `legacy_org_mapping`: all ETBC org IDs exist and map to IAM orgs.

Relationship integrity:

- `iam_user_role`: no orphan user IDs or role IDs.
- `iam_role_permission`: no orphan role IDs or permission IDs.
- `iam_feature_permission`: no orphan feature IDs or permission IDs.
- `iam_solution_layout`: resourceId and parentResourceId are valid; tree has no cycles.

Menu tree equivalence (via legacy mapping):

- Parent-child structure matches ETBC tree.
- Sibling order matches ETBC sort/order.
- Visible nodes match ETBC visibility rules.

## Authentication checks

- Successful login for a sample set of active users across password algorithms.
- Verify session and user identity from `iam-management-service` portal endpoints.
- Negative cases: disabled, locked, expired, wrong password.

Recommended coverage:

- High-privilege users
- Standard users with limited menus
- Users with no permissions
- Edge cases with special characters in username/password

## Authorization and menu checks

- Fetch portal-visible apps/menus/permissions for each sample user.
- Map IAM resource IDs back to ETBC using `legacy_resource_mapping`.
- Diff against baseline: missing nodes, extra nodes, permission mismatches.
- Validate protected API calls (via APISIX) return expected 200/403 outcomes.

## UI checks (portal)

- Automate login and validate landing page.
- Validate menu tree rendering and expansion for each sample user.
- Validate key routes load successfully (no 403/404).

## Report fields

- environment, timestamp, git refs/versions, tenantId
- total_users_tested, login_failures
- missing_mappings_count, duplicate_mappings_count
- permission_diffs_count, menu_diffs_count
- api_authorization_failures
- ui_failures
- blocking_status (pass/fail) and thresholds
