# Implementation Plan Content Type

## Detection

- Extensions: No specific extension.
- Heuristics: `.md` file with 3+ `<task>` tags at line start outside code blocks.
- Override keyword: `plan`

## Issue Types

### Type-Specific Issues

| Type | Description | Severity | Auto-fixable |
|------|-------------|----------|--------------|
| `missing_verification` | Task has no verification/verify step | Critical | No |
| `missing_done_criteria` | Task has no done/completion criteria | Critical | No |
| `vague_action` | Action is not specific enough to execute | Major | No |
| `undefined_dependency` | Depends on something unspecified | Major | No |
| `missing_files_list` | No files list for a task that modifies files | Major | No |
| `unmeasurable_success` | Success criteria not objectively testable | Major | No |

### Severity Overrides (from base)

- `vague_instruction`: Critical (reason: in plans, vague instructions cause implementation failures — agents cannot execute ambiguous steps)

### Auto-fixable Overrides (from base)

None.

## Detection Patterns

### missing_verification

Look for:
- Tasks/steps with no `<verify>` or verification section
- Tasks that create or modify files with no way to confirm success
- Steps that say "ensure" or "make sure" without specifying how to verify

### missing_done_criteria

Look for:
- Tasks with no `<done>` tag or done criteria section
- Steps with no measurable completion indicator
- Tasks where completion is ambiguous ("improve performance")

### vague_action

Look for:
- "Set up the environment" (which environment? what steps?)
- "Configure properly" / "Handle correctly"
- "Update as needed" / "Fix if necessary"
- Actions using verbs without concrete objects or outcomes
- Steps that require the implementer to make unstated decisions

### undefined_dependency

Look for:
- References to tasks, tools, or systems not defined in the plan
- "After X is ready" where X is not a defined task
- Implicit ordering without explicit dependency declarations
- External tools or services mentioned but not specified

### missing_files_list

Look for:
- Tasks that describe creating or modifying code with no file paths
- Steps mentioning "update the component" without specifying which file
- Implementation tasks with no `<files>` section listing affected files

### unmeasurable_success

Look for:
- "Should work correctly" (how to verify?)
- "Performance should be acceptable" (what threshold?)
- "Users should be satisfied" (no metric)
- Success criteria using subjective language
- Criteria that cannot be automated or objectively checked

## Mode Adjustments

### Aggressive

- Flag any task without explicit verification steps
- Flag any action that requires implementer judgment
- Flag missing file lists even for documentation-only tasks
- Escalate `vague_action` to Critical
- Flag implicit dependencies between tasks

### Conservative

- Skip `missing_files_list` (implementer may know the codebase)
- Skip `unmeasurable_success` (some criteria are inherently qualitative)
- Still flag `missing_verification` and `missing_done_criteria` (critical for autonomous execution)
- Still flag `vague_action` (blocks implementation)
- Still flag `undefined_dependency` (blocks task ordering)

## Codex Prompt Extension

9. Tasks missing verification or done criteria
10. Vague actions that cannot be executed without guessing
11. Undefined dependencies between tasks
12. Success criteria that cannot be objectively measured
