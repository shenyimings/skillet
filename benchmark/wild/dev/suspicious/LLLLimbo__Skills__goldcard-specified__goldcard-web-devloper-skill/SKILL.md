---
name: goldcard-web-devloper-skill
description: Gold Card (金卡) web frontend developer guidelines covering component library docs, coding standards, and portal identity center design. Use when working on Gold Card frontend components, applying 金卡前端编码规范, or integrating with the portal/identity center.
---

# Goldcard Web Developer Skill

## Overview

Use these references to implement Gold Card frontend features with the approved component library, coding standards, and portal identity center design patterns.

## When to use

## Quick start

1. Identify whether the task is component usage, coding standards, or portal integration.
2. Open the matching reference file(s) listed below.
3. Follow the doc's API, props, and demo patterns; reuse existing examples where possible.

## Reference map

- Component library: `references/components/`
  - Web components, directives, utilities, and presets in `references/components/web/`
  - Mobile components in `references/components/mobile/`
  - JS-bridge docs in `references/components/js-bridge/`
  - CLI/i18n docs in `references/components/cli/`
  - Open API docs in `references/components/open-api/`
  - Three.js docs in `references/components/threejs/`
- Coding standards: `references/rule/code/index.md` (examples in `references/rule/code/demo1.vue`)
- Portal design (Identity Center): `references/scheme/identityCenter.md`

## Repositories

- Portal frontend: `http://10.200.1.145/web/platform/portal-front.git` (branch: `dev`)
- Operations management system frontend: `http://10.200.1.145/web/platform/operations-management-system.git` (branch: `dev`)

## Usage notes

- Prefer each component's `index.md` for the main API and usage, then consult demo `.vue`/`.js` files for concrete patterns.
- Treat the coding standards as source-of-truth for naming, project structure, and Vue 3 + Vite defaults.
- Resolve portal integration helpers like `microAppInit` via `references/components/web/utils/`.
- Note that some docs link to internal URLs; treat them as references if the links are not reachable.

## Search tips

- Find a component or directive: `rg -n "ui-" references/components`
- Find a specific prop or API: `rg -n "props|emit|event" references/components`
- Find portal integration mentions: `rg -n "portal|microApp|postMessage" references`
