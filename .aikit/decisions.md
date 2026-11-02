# Decisions

Why this project is built the way it is, oldest first. One entry per decision that changes a
contract, a dependency, a data format or the architecture; IDs are consecutive and never reused.

### ADR-001: Signal Garden brief builder refinement with acronym preservation, domain milestones, stdin streaming, and markdown/aikit export
- **Date**: 2026-11-01
- **Status**: Accepted
- **Context**: The initial brief builder destroyed uppercase acronyms (REST, API, OAuth2) via naive capitalization, generated static generic milestones regardless of goal context, had a narrow 5-term risk taxonomy, and lacked stdin pipe streaming or markdown/AIKit plan exports.
- **Decision**: Preserve casing of all words while capitalizing the initial character of the first word; expand risk taxonomy to 10 core engineering vectors with keyword aliases; tailor the 4 delivery milestones dynamically to detected domains; support stdin piping via `-` or redirected input; add `--markdown` for GitHub Flavored Markdown brief rendering; and provide `--aikit` to synthesize runnable AIKit checkpoint commands.
- **Consequences**: Existing tests continue to pass with backward-compatible Brief dict representations; brief outputs become significantly more actionable and integrated with AIKit workflows; requires 0 external dependencies (Python standard library only).

### ADR-002: Token-boundary risk detection replacing substring matching
- **Date**: 2026-11-03
- **Status**: Accepted
- **Context**: Risk detection used `term in lowered` substring checks, causing false positives (`db` in `sandbox`, `api` in `rapid`, `perf` in `superficial`, `auth` in `author`) while missing legitimate derivations (`authentication`, `performance`, `https`, `mysql`/`postgresql`/`sqlite`).
- **Decision**: Tokenize goals with `re.findall(r"[a-z0-9]+", lowered)` and match against an explicit `RISK_TOKEN_VARIANTS` map per risk key (base terms plus curated inflections, verb forms, plurals, and DB aliases); `RISK_TERMS`/`RISK_ALIASES` retained for taxonomy reference.
- **Consequences**: `sandbox`/`rapid`/`superficial`/`author` goals now correctly report no keyword risk; `authentication`, `performance`, `https`/`apis`, and `mysql`/`postgresql`/`sqlite` still trigger their vectors; Brief dict schema unchanged; 2 new failing-first tests added.

### ADR-003: Token-boundary milestone tailoring aligned with risk variants
- **Date**: 2026-11-03
- **Status**: Accepted
- **Context**: `_tailor_milestones` used the same substring checks, so `sandbox` got data-schema M1, `rapid` got network M3, and `superficial` got resource-bounded M2, while `scaling` missed the perf M2 and `caching`/`mysql` missed the data M1.
- **Decision**: Tailor milestones from the same token set, reusing `RISK_TOKEN_VARIANTS` for auth/payment/network/perf plus a `_DATA_MILESTONE_TOKENS` group (`data`, `dataset(s)`, `metadata`, `datastore` plus database and migration variants); milestone text and 4-item contract unchanged.
- **Consequences**: Generic goals keep generic milestones; `scaling` yields resource-bounded M2 and `caching`/`mysql` yield data-schema M1; `authentication` still yields auth milestones; 2 new failing-first tests added.

### ADR-004: Shell-safe AIKit checkpoint export via backslash/quote escaping
- **Date**: 2026-11-03
- **Status**: Accepted
- **Context**: `to_aikit_checkpoint` interpolated goal/summary/title/risks into double-quoted shell fragments but escaped quotes only in risks, so a goal like `ship "quoted" auth service` produced broken `--why "ship "quoted" auth service"` and backslashes passed through unescaped.
- **Decision**: Add `_shell_escape` (escape `\` then `"`) and apply it to title, goal, summary, and risks in `to_aikit_checkpoint`; CLI flags and output format unchanged.
- **Consequences**: Quoted and Windows-path goals now emit parseable checkpoint commands; existing `--aikit` consumers see only corrected quoting for previously broken inputs; 2 new failing-first tests added.
