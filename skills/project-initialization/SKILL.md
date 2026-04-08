---
name: project-initialization
description: Create a standardized analysis-project directory tree. Use when the user asks to "\u521b\u5efa\u5206\u6790\u9879\u76ee\u7684\u5185\u5bb9" (Chinese phrase for creating analysis project content) or requests initialization of a new analysis project folder. Prompt the user for the project root name, prepend the next two-digit sequence as `0X-`, then create the root folder and five fixed subfolders.
---

# Project Initialization Skill

Initialize analysis project folders with deterministic naming and structure.

## Workflow

1. Detect trigger intent:
   - Use this skill when the user says `\u521b\u5efa\u5206\u6790\u9879\u76ee\u7684\u5185\u5bb9` or asks to initialize an analysis project directory.
2. Request the project root name from the user:
   - Ask for a single name value.
   - Remind the user that a two-digit sequence prefix (`0X-`) will be prepended automatically.
3. Build the final root directory name:
   - Scan existing sibling project folders in the target parent directory.
   - Detect leading two-digit prefixes matching `^\d{2}-`.
   - Find the maximum existing prefix number, then increment by 1.
   - Format as two digits (e.g., `01`, `02`, `03`, ...).
   - Create final name as `<next_2_digit>-<input_name>`.
   - Example: existing `01-aaa`, `02-bbb`, `03-ccc`; input `temp_test` -> output `04-temp_test`.
4. Create the root directory and fixed subdirectories:
   - `01-code`
   - `02-Rawdata`
   - `03-output`
   - `04-files`
   - `05-source`
5. Confirm completion:
   - Return the created root directory name and list created subdirectories.

## Execution Notes

- Keep the user's input name unchanged except trimming surrounding spaces.
- Always prepend the computed two-digit sequence prefix and hyphen.
- If no existing prefixed project folder is found, start from `01-`.
- Use these exact subdirectory names and ordering.

## Output Contract

- Root directory: `<next_2_digit>-<user_name>`
- Subdirectories:
  - `01-code`
  - `02-Rawdata`
  - `03-output`
  - `04-files`
  - `05-source`
