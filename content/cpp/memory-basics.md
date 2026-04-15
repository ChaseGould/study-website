# C++ Memory Basics

Pointers store addresses, while references act like stable aliases to existing values.

## Quick rules
- Prefer stack allocation when ownership is simple.
- Use `std::unique_ptr` when one object clearly owns another.
- Avoid raw `new` in everyday application code.

## Why this matters
Memory bugs are often harder to debug than syntax errors because the program may fail far away from the original mistake.
