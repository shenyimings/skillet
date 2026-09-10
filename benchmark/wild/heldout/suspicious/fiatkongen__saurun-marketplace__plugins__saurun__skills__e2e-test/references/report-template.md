# E2E Report Template

Write report to `{RESULTS_DIR}/report.md` using this template:

```markdown
# E2E Test Results

## Summary
- **Total flows tested:** {n}
- **Passed:** {n}
- **Fixed (auto):** {n}
- **Unresolved:** {n}
- **Run time:** {duration}

## Videos (Demo Artifacts)
| User Flow | Status | Video |
|-----------|--------|-------|
| {name} | ✅ Passed | [video](videos/{name}.webm) |
| {name} | 🔧 Fixed | [video](videos/{name}.webm) |
| {name} | ❌ Failed | [video](videos/{name}.webm) |

## Fix Attempts Log

### {Test Name} (Fixed on attempt {n})
- **Attempt 1:** Diagnosed as `{category}` — {description}. Fixed `{file}:{line}`.

### {Test Name} (Unresolved after 3 attempts)
- **Attempt 1:** {diagnosis and action}
- **Attempt 2:** {diagnosis and action}
- **Attempt 3:** {diagnosis and action}
- **Root cause:** {best hypothesis}

## Unresolved Failures
| Test | Category | Error | Attempts |
|------|----------|-------|----------|
| {name} | {category} | {error summary} | 3 |

## Failure Categories
| Category | Count | Notes |
|----------|-------|-------|
| `infra` | {n} | Environment/startup issues |
| `app-code` | {n} | Application bugs |
| `test-code` | {n} | Test selector/logic issues |
| `flaky` | {n} | Intermittent failures |
```
