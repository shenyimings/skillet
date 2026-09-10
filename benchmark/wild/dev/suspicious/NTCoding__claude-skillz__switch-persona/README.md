# Switch Persona Skill

Quick mid-conversation persona switching without restarting Claude.

## What It Does

Changes Claude's system instructions during an active conversation:
- **Preserves** conversation history
- **Replaces** system instructions completely
- **No restart required**
- **No confirmations** - immediate switch

## Triggers

User says:
- "switch persona"
- "switch to [name]"
- "become [name]"

## How It Works

### With specific persona name:
1. Reads `~/.claude/system-prompts/[name].txt` (or `.md`)
2. Adopts new persona instructions
3. Announces switch and continues as new persona

### Without specific name:
1. Lists available personas from `~/.claude/system-prompts/`
2. User selects by number or name
3. Reads selected persona file
4. Announces switch and continues as new persona

## Key Principle

**One persona at a time - complete replacement.**

Each switch fully replaces the previous persona. You cannot blend multiple personas simultaneously. Want combined traits? Create a custom system prompt.

## File Locations

**Personas:** `~/.claude/system-prompts/` (`.txt` or `.md`)

## Installation

Symlink to Claude skills directory:

```bash
ln -s /path/to/claude-skillz/switch-persona ~/.claude/skills/switch-persona
```

## Integration with claude-launcher

| Feature | claude-launcher | switch-persona |
|---------|----------------|----------------|
| **When** | Startup | Runtime |
| **Context** | New conversation | Preserves conversation |
| **How** | CLI tool | Skill |

**Use together:**
- claude-launcher: Choose initial persona
- switch-persona: Change mid-conversation
- Both read from same `~/.claude/system-prompts/` directory
