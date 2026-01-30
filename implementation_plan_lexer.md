
# Implementation Plan - Fix Context Blindness in Lexer

## User Review Required
> [!IMPORTANT]
> This change modifies the `Lexer` to track bracket depth. `INDENT`, `DEDENT`, and `NEWLINE` tokens will be suppressed when inside open brackets `(`, `[`, `{`. This allows for multi-line lists, function calls, and dictionaries without breaking the geometric parsing logic.

## Proposed Changes

### [shell_lite]

#### [MODIFY] [lexer.py](file:///c:/Users/shrey/OneDrive/Desktop/oka/shell-lite-llvm/shell_lite/lexer.py)
- Add `self.bracket_depth = 0` to `__init__`.
- Update `tokenize_line` to increment/decrement `bracket_depth` on `(`, `[`, `{` and `)`, `]`, `}`.
- Modify the main `tokenize` loop to **skip** generating `INDENT`, `DEDENT`, and `NEWLINE` tokens if `self.bracket_depth > 0`.
- This ensures that physically multiple lines inside brackets are treated as a single logical line by the GBP parser.

## Verification Plan

### Automated Tests
- Run `tests/repro_context.py` again.
- Expectation:
    - No `INDENT`/`DEDENT` tokens inside the list.
    - `NEWLINE` tokens inside the list should also be ignored or handled such that the parser sees one continuous stream of tokens for the assignment.
    - The `bind_assignment` method in `parser_gbp.py` handles the tokens properly. *Note: `bind_assignment` might also need a tweak to consume the full list if it stops at the first newline, but fixing the lexer is step 1.*
