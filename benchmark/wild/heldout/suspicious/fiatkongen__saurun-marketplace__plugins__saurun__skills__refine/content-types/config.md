# Configuration Content Type

## Detection

- Extensions: `.yaml`, `.yml`, `.json`, `.toml`, `.ini`, `.env`
- Heuristics: None — extension match is sufficient.
- Override keyword: `config`

## Issue Types

### Type-Specific Issues

| Type | Description | Severity | Auto-fixable |
|------|-------------|----------|--------------|
| `duplicate_key` | Same key appears twice in the same scope | Critical | Yes |
| `type_mismatch` | Value type doesn't match expected type | Critical | No |
| `missing_required_field` | Schema-required field is absent | Critical | No |
| `unused_variable` | Defined but never referenced | Minor | No |
| `inconsistent_indentation` | Mixed indentation styles (2-space vs 4-space) | Minor | Yes |
| `no_default_value` | Optional field with no default specified | Minor | No |

### Severity Overrides (from base)

- `trailing_whitespace`: Major (reason: trailing whitespace in YAML can affect semantics — trailing spaces change string values)
- `formatting_inconsistency`: Major (reason: inconsistent formatting in YAML/TOML affects readability and can cause parsing issues with strict parsers)

### Auto-fixable Overrides (from base)

None.

## Detection Patterns

### duplicate_key

Look for:
- Same key name at the same nesting level
- YAML: duplicate keys are silently overwritten (last wins)
- JSON: duplicate keys are technically invalid per RFC 7159
- TOML: duplicate keys are a parse error
- Check nested objects separately (same key in different parents is fine)

### type_mismatch

Look for:
- String where number expected: `port: "8080"` instead of `port: 8080`
- Number where boolean expected: `enabled: 1` instead of `enabled: true`
- String where array expected: `hosts: "localhost"` instead of `hosts: ["localhost"]`
- Compare against schema if available, or infer from key name conventions

### missing_required_field

Look for:
- Common required fields missing: `name`, `version` in package configs
- Database configs without `host` or `port`
- Auth configs without `secret` or `key`
- Infer from context what fields are likely required

### unused_variable

Look for:
- Environment variables defined but not referenced in config
- YAML anchors (`&anchor`) defined but never aliased (`*anchor`)
- Variables in `.env` files not used by the application config
- Note: cross-file usage may make this a false positive — flag with low confidence

### inconsistent_indentation

Look for:
- Mixed 2-space and 4-space indentation in YAML
- Tabs mixed with spaces
- Inconsistent nesting depth for same-level items
- JSON with mixed indentation (though auto-formatters usually handle this)

### no_default_value

Look for:
- Optional fields with no default in schema or comments
- Environment variables without fallback values
- Config keys that would cause errors if omitted and no default exists

## Mode Adjustments

### Aggressive

- Flag all duplicate keys even in deeply nested structures
- Flag all type mismatches even when implicit conversion works
- Flag unused variables even when cross-file usage is possible
- Flag `no_default_value` for all optional fields
- Flag inconsistent indentation even when parseable

### Conservative

- Skip `unused_variable` (cross-file usage likely)
- Skip `no_default_value` (defaults may be in application code)
- Skip `inconsistent_indentation` (parsers handle it)
- Still flag `duplicate_key` (silent data loss)
- Still flag `type_mismatch` (runtime errors)
- Still flag `missing_required_field` (prevents startup)

## Codex Prompt Extension

9. Duplicate keys at the same nesting level
10. Type mismatches (string where number expected, etc.)
11. Missing required fields (name, version, host, port, etc.)
12. Inconsistent indentation within the same file
