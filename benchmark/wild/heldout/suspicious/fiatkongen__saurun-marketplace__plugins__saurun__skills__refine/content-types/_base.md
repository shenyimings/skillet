# Base Content Type (Universal)

## Detection

None — always loaded. Every content type inherits these universal issues.

## Issue Type Enumeration

Formal list of valid `type` values for issue objects. All issue-finder output and codex-validator input/output must use these types.

| Type | Description | Severity | Auto-fixable |
|------|-------------|----------|--------------|
| `vague_instruction` | Instruction lacks specificity, reader must guess | Major | No |
| `ambiguous_scope` | Could mean multiple things, unclear boundaries | Major | No |
| `unresolved_todo` | TODO/TBD/FIXME/??? placeholder remaining | Major | No |
| `inconsistent_terminology` | Same concept, different names throughout | Major | Conditional (>70% dominant -> auto, else ask) |
| `broken_reference` | Link to non-existent target (section, file) | Critical | Sometimes (if target found elsewhere) |
| `redundant_content` | Same information repeated unnecessarily | Major | Yes |
| `formatting_inconsistency` | Mixed styles (bullets, headings, etc.) | Minor | Yes |
| `missing_definition` | Term used but never defined | Critical | No |
| `contradiction` | Two statements that conflict | Critical | No |
| `trailing_whitespace` | Extra spaces, unnecessary blank lines | Minor | Yes |
| `incomplete_list` | Single-item list that should be prose | Minor | Yes |
| `missing_context` | Assumes knowledge not provided | Major | No |
| `inconsistent_casing` | Mixed case for same term (API vs Api vs api) | Minor | Yes |

### Usage Notes

- **issue-finder** must set `type` field using values from this enum
- **codex-validator** must validate that incoming issues have valid types
- **SKILL.md Phase 3** switches on `type` to determine prompt strategy
- Unknown types should be logged and treated as `auto_fixable: false`
- Content-type files may add new types not listed here
- Content-type files may override severity and auto-fixable for base types (type wins on conflict)

## Issue Types

### Critical Severity

| Issue | Description | Example | Auto-fixable |
|-------|-------------|---------|--------------|
| Contradiction | Two statements that conflict | "Always use X" then later "Never use X" | No |
| Broken reference | Links to non-existent target | `[see above](#nonexistent)` | Sometimes |
| Missing definition | Term used but never defined | "Configure the FrobNozzle" (never explained) | No |

### Major Severity

| Issue | Description | Example | Auto-fixable |
|-------|-------------|---------|--------------|
| Inconsistent terminology | Same concept, different names | "user" vs "customer" vs "client" | Conditional |
| Vague instruction | Reader must guess intent | "Handle errors appropriately" | No |
| Unresolved placeholder | TODO/TBD/??? remaining | "TODO: add details" | No |
| Redundant content | Same info repeated | Paragraph A says same as paragraph B | Yes |
| Ambiguous scope | Could mean multiple things | "Update the configuration" (which one?) | No |
| Missing context | Assumes knowledge not provided | References internal system without explanation | No |

### Minor Severity

| Issue | Description | Example | Auto-fixable |
|-------|-------------|---------|--------------|
| Formatting inconsistency | Mixed styles | Bullets: `-`, `*`, `+` mixed | Yes |
| Incomplete list | List with one item | `- Only item` | Yes |
| Trailing whitespace | Extra spaces | Lines ending with spaces | Yes |
| Inconsistent casing | Mixed case for same term | "API" vs "Api" vs "api" | Yes |

## auto_fixable Rules

Set `auto_fixable: true` ONLY when fix is unambiguous:
- Terminology with >70% dominant term -> true
- Redundant paragraph (clear duplicate) -> true
- Mixed bullet markers -> true
- Trailing whitespace -> true
- Single-item list -> true
- Inconsistent casing (authoritative form identifiable) -> true
- Everything else -> false

**When in doubt, set false.** Better to ask the user than silently make a wrong fix.

## Detection Patterns

### Vague Instructions

Look for:
- "appropriately", "properly", "correctly"
- "as needed", "if necessary", "when required"
- "handle", "manage", "process" without specifics
- "etc.", "and so on", "and more"
- Passive voice without actor: "should be validated"

### Inconsistent Terminology

Check for:
- Same concept: user/customer/client, app/application, config/configuration
- Abbreviations: API/api, URL/url, DB/database
- British/American: colour/color, behaviour/behavior
- Pluralization: data is/data are

### Redundant Content

Patterns:
- Two paragraphs saying the same thing differently
- Bullet point that restates the heading
- "In other words..." followed by repetition
- Summary that just repeats previous sections

### Ambiguous Scope

Signals:
- "the configuration" (which one?)
- "update the file" (which file?)
- "this should work" (what conditions?)
- Pronouns with unclear antecedents

### Inconsistent Casing

Patterns:
- Same term in different cases: "API" vs "Api" vs "api"
- Acronyms inconsistently capitalized
- Proper nouns with varying capitalization
- Technical terms with unstable casing (e.g., "GitHub" vs "Github" vs "github")

## Mode Adjustments

### Default Mode

**Flag**: All Critical, all Major
**Auto-fix**: Formatting, clear inconsistencies
**Ask user**: Vague content, ambiguities, TODOs

### Aggressive Mode

**Flag**: All Critical, all Major, all Minor
**Auto-fix**: Everything possible
**Additional actions**:
- Remove verbose explanations
- Tighten prose
- Eliminate redundancy aggressively
- Suggest restructuring

### Conservative Mode

**Flag**: Critical + Ambiguities requiring user input
**Auto-fix**: Only clear errors (no subjective improvements)
**Preserve**:
- Author's style choices
- Verbose explanations (may be intentional)
- Structural decisions
- Minor formatting differences

**Note**: Conservative mode still flags vague instructions, unclear scope, and TODOs because these need user resolution. It just skips minor formatting issues.

## Codex Prompt

LOOK FOR:
1. Vague instructions (reader must guess intent)
2. Inconsistent terminology (same concept, different names)
3. Missing information (referenced but not defined)
4. Redundant content (same thing said multiple ways)
5. Unclear scope (ambiguous boundaries)
6. Broken references (links to non-existent things)
7. Unresolved placeholders (TODOs, TBDs)
8. Inconsistent casing (same term in different cases: API vs Api vs api)

DO NOT FLAG:
- Stylistic preferences (unless inconsistent)
- Subjective 'could be better' suggestions
- Things already fixed
