---
name: sql-code-style
description: Use when writing, refactoring, or reviewing SQL that should follow a consistent, business-agnostic style with layered structure, low duplication, and clear rationale for any rule deviations.
---

# SQL Code Style

## Overview
Apply a business-agnostic SQL writing system that prioritizes readability, composability, deterministic aggregation, and maintainability. Use ANSI-first patterns by default and keep dialect-specific behavior isolated.

## Style Principles
- Optimize for human review first: stable layout, explicit naming, and predictable section order.
- Compose queries in layers so each block has one purpose and one output grain.
- Make aggregation deterministic by defining keys and grain before metrics.
- Minimize duplication by centralizing repeated logic (classification rules, filters, derived dimensions).
- Prefer explicitness over terseness for joins, null handling, and metric definitions.

## Authoring Workflow
1. Define output grain and required columns before writing SQL.
2. Build a query skeleton with staged CTEs (or equivalent subquery layers).
3. Isolate dimensions/keys in foundational layers.
4. Add metric blocks grouped by subject, each aligned to the same grain.
5. Assemble the final wide result with explicit join keys.
6. Run checklist-based review and document justified deviations.

## Rules (Hard vs Soft)
### Hard Rules
- Declare and preserve grain explicitly at every layer.
- Keep join predicates explicit; never rely on implicit join behavior.
- Keep metric names and aliases stable and self-describing.
- Prevent mixed-grain aggregation in the same SELECT block.
- Use null-safe defaults where missing data changes metric meaning.

### Soft Rules (Guided but Flexible)
- Prefer CTE layering over deeply nested subqueries.
- Keep line-level formatting consistent across blocks.
- Keep one logical responsibility per CTE.
- If a soft rule is violated, include a brief rationale and impact note.

## Reusable Patterns
- CTE layering: base keys -> dimensions -> metric blocks -> final select.
- Key alignment: join only on declared grain keys.
- Conditional aggregation: standard CASE-in-aggregate patterns.
- Null safety: COALESCE at metric boundaries, not indiscriminately.

For concrete templates, see [references/patterns.md](references/patterns.md).

## Anti-Patterns
- Copy-pasted CASE logic across multiple blocks.
- Hidden filters spread across unrelated layers.
- Alias drift where the same concept has multiple names.
- Mixing row-level and aggregated fields without explicit staging.
- Dialect-specific constructs in core logic when ANSI alternatives exist.

## Review Checklist
- Is the output grain explicitly stated and preserved?
- Are all joins explicit and key-aligned?
- Are repeated rules centralized instead of duplicated?
- Are metric definitions deterministic and null-safe?
- Is formatting consistent and readable?
- Are any deviations documented with rationale and impact?
- Is the core query portable (ANSI-first), with dialect notes isolated?

