# Code Content Type

## Detection

- Extensions: `.ts`, `.js`, `.tsx`, `.jsx`, `.cs`, `.py`, `.go`, `.rs`, `.java`, `.rb`, `.swift`, `.kt`
- Heuristics: None — extension match is sufficient.
- Override keyword: `code`

## Issue Types

### Type-Specific Issues

| Type | Description | Severity | Auto-fixable |
|------|-------------|----------|--------------|
| `naming_inconsistency` | Mixed naming conventions (camelCase vs snake_case) | Major | Yes |
| `stale_comment` | Comment doesn't match the code it describes | Major | No (if unclear whether stale, set auto_fixable=false) |
| `dead_code` | Unreachable or unused code | Minor | Yes |
| `missing_type` | No type annotation where expected | Minor | No |
| `magic_number` | Unexplained numeric literal | Minor | No |

### Severity Overrides (from base)

None.

### Auto-fixable Overrides (from base)

None.

## Detection Patterns

### naming_inconsistency

Look for:
- camelCase and snake_case mixed in the same scope
- PascalCase for non-class identifiers (or vice versa)
- SCREAMING_CASE for non-constants
- Inconsistency within a single file (compare function names, variable names, parameter names)
- Identify the dominant convention and flag deviations

### stale_comment

Look for:
- Comments describing behavior the code no longer implements
- Parameter names in JSDoc/docstrings that don't match actual parameters
- Comments referencing removed variables, functions, or imports
- "TODO: done" or similar contradictions
- Comments above a function that describe a different function's behavior

### dead_code

Look for:
- Functions/methods never called within the file (and not exported)
- Variables assigned but never read
- Code after unconditional `return`, `throw`, `break`, `continue`
- Commented-out code blocks
- Unreachable branches (e.g., `if (false) { ... }`)

### missing_type

Look for:
- Function parameters without type annotations (in typed languages)
- Return types not specified (TypeScript, Python with type hints)
- Variables with `any` type that could be narrowed
- Note: respect language conventions (Python doesn't always require types)

### magic_number

Look for:
- Numeric literals in conditionals: `if (x > 86400)`
- Array indices beyond 0/1: `items[42]`
- Math operations with unexplained constants
- Exceptions: 0, 1, -1, 2 (common in loops/checks), HTTP status codes in context

## Mode Adjustments

### Aggressive

- Flag all naming deviations from the dominant convention
- Flag all magic numbers including common ones
- Flag all missing types
- Flag dead code including potentially unused exports
- Flag stale comments including borderline cases

### Conservative

- Skip `dead_code` (may be used externally or kept intentionally)
- Skip `magic_number` (may be well-understood in context)
- Skip `missing_type` (may follow language idioms)
- Still flag `naming_inconsistency` (objective, verifiable)
- Still flag `stale_comment` (actively misleading)

## Codex Prompt Extension

9. Naming convention violations (mixed camelCase/snake_case in same scope)
10. Comments that contradict the code they describe
11. Unreachable or demonstrably unused code
12. Unexplained numeric literals (magic numbers)
