# Markdown Content Type

## Detection

- Extensions: `.md`
- Heuristics: Default for `.md` files. Overridden by `plan` if file contains 3+ `<task>` tags at line start outside code blocks.
- Override keyword: `markdown`

## Issue Types

### Type-Specific Issues

| Type | Description | Severity | Auto-fixable |
|------|-------------|----------|--------------|
| `heading_skip` | Heading level skipped (e.g., h1 -> h3) | Minor | Yes |
| `orphan_heading` | Heading with no content below it | Major | No |
| `broken_reference` | Internal link to missing section/anchor (extends base `broken_reference` for markdown-specific patterns) | Critical | No |
| `unclosed_formatting` | Formatting marker without closing pair | Critical | Yes |
| `mixed_list_markers` | Different markers in the same list | Minor | Yes |
| `code_block_no_language` | Fenced code block without language tag | Minor | Yes |

### Severity Overrides (from base)

None.

### Auto-fixable Overrides (from base)

None.

## Detection Patterns

### heading_skip

Look for heading level jumps:
- `# Title` followed by `### Subsection` (skipped h2)
- Any `#` heading followed by a heading 2+ levels deeper
- Check the full heading hierarchy from top to bottom

### orphan_heading

Look for:
- Heading immediately followed by another heading (no content between)
- Heading at end of file with no content after
- Exception: headings that serve as section dividers by convention (e.g., `## ---`)

### broken_reference (markdown-specific patterns)

In addition to the base `broken_reference` detection, look for:
- `[text](#anchor)` where no heading generates that anchor
- `[text](relative/path.md)` where no such file is referenced elsewhere
- Anchor format: lowercase, spaces replaced with hyphens, special chars removed

### unclosed_formatting

Look for:
- `**bold without closing **`
- `*italic without closing *`
- `` `code without closing ` ``
- `~~strikethrough without closing ~~`
- Count opening and closing markers per line/paragraph

### mixed_list_markers

Look for:
- `-` and `*` in the same list block
- `-` and `+` in the same list block
- Numbered and unnumbered items mixed without nesting

### code_block_no_language

Look for:
- ` ``` ` without a language identifier on the opening fence
- Exception: code blocks containing plain text or output (no syntax to highlight)

## Mode Adjustments

### Aggressive

- Flag all heading skips even if only one level
- Flag code blocks without language even when content is ambiguous
- Flag orphan headings even if they might be intentional placeholders
- Suggest removing empty sections

### Conservative

- Skip `heading_skip` (may be intentional structure)
- Skip `code_block_no_language` (may be intentional plain text)
- Skip `mixed_list_markers` (may be intentional visual distinction)
- Still flag `broken_reference` and `unclosed_formatting` (objective errors)

## Codex Prompt Extension

9. Heading hierarchy violations (h1 -> h3 skipping h2)
10. Internal links pointing to non-existent anchors
11. Unclosed markdown formatting (bold, italic, code)
12. Malformed or empty table cells
