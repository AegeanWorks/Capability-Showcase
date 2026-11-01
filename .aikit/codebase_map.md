# Codebase Map & Symbol Catalog 🗺️

> **AUTO-GENERATED & VERIFIED BY `scripts/update_knowledge_base.py`**
> This document provides an automated, up-to-date registry of all modules, classes, and exported functions across this repository.

---

## 📊 Codebase Metrics
- **Total Python Modules**: `2`
- **Total Classes**: `2`
- **Total Top-Level Functions**: `4`
- **Total Class Methods**: `5`
- **Total Source Lines**: `140`

---

## 📦 Modules & Exported Symbols

### [`signal_garden.py`](signal_garden.py)
> *Turn a plain-text goal into a small, deterministic execution brief.*

**Size**: `100` lines (`3112` bytes)

**Classes:**
- `class Brief`
  - Method `.as_dict()`

**Functions:**
- `def _title(goal)`
- `def build_brief(goal)` - *Build a bounded brief without network access or hidden state.*
- `def _parser()`
- `def main(argv)`

---

### [`tests/test_signal_garden.py`](tests/test_signal_garden.py)
**Size**: `40` lines (`1270` bytes)

**Classes:**
- `class SignalGardenTests`
  - Method `.test_build_brief_normalizes_goal_and_detects_risk()`
  - Method `.test_long_goals_are_marked_expanded()`
  - Method `.test_empty_goal_is_rejected()`
  - Method `.test_json_mode_is_machine_readable()`

---
