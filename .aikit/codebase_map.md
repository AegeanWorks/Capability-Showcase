# Codebase Map & Symbol Catalog 🗺️

> **AUTO-GENERATED & VERIFIED BY `scripts/update_knowledge_base.py`**
> This document provides an automated, up-to-date registry of all modules, classes, and exported functions across this repository.

---

## 📊 Codebase Metrics
- **Total Python Modules**: `2`
- **Total Classes**: `2`
- **Total Top-Level Functions**: `8`
- **Total Class Methods**: `22`
- **Total Source Lines**: `491`

---

## 📦 Modules & Exported Symbols

### [`signal_garden.py`](signal_garden.py)
> *Turn a plain-text goal into a small, deterministic execution brief.*

**Size**: `312` lines (`11527` bytes)

**Classes:**
- `class Brief`
  - Method `.as_dict()`
  - Method `.to_markdown()`
  - Method `.to_aikit_checkpoint(task_id)`

**Functions:**
- `def _word_tokens(lowered)`
- `def _shell_escape(value)`
- `def _title(goal)`
- `def _tailor_milestones(lowered)`
- `def build_brief(goal)` - *Build a bounded brief without network access or hidden state.*
- `def _parser()`
- `def _read_goal(args_goal)`
- `def main(argv)`

---

### [`tests/test_signal_garden.py`](tests/test_signal_garden.py)
**Size**: `179` lines (`7622` bytes)

**Classes:**
- `class SignalGardenTests`
  - Method `.test_build_brief_normalizes_goal_and_detects_risk()`
  - Method `.test_long_goals_are_marked_expanded()`
  - Method `.test_empty_goal_is_rejected()`
  - Method `.test_json_mode_is_machine_readable()`
  - Method `.test_title_preserves_acronyms_and_special_casing()`
  - Method `.test_expanded_risk_taxonomy()`
  - Method `.test_domain_aware_milestone_tailoring()`
  - Method `.test_markdown_mode_formatting()`
  - Method `.test_aikit_checkpoint_export()`
  - Method `.test_stdin_pipe_support()`
  - Method `.test_goal_length_bound()`
  - Method `.test_error_triad_output_on_invalid_goal()`
  - Method `.test_wave10_no_substring_false_positives()`
  - Method `.test_wave10_legitimate_variants_still_detected()`
  - Method `.test_wave20_milestone_no_false_positives()`
  - Method `.test_wave20_milestone_legitimate_variants()`
  - Method `.test_wave30_aikit_checkpoint_escapes_quotes()`
  - Method `.test_wave30_aikit_checkpoint_escapes_backslash()`
  - Method `.test_wave31_oauth_variants_detected()`

---
