# Decisions

Why this project is built the way it is, oldest first. One entry per decision that changes a
contract, a dependency, a data format or the architecture; IDs are consecutive and never reused.

### ADR-001: Signal Garden brief builder refinement with acronym preservation, domain milestones, stdin streaming, and markdown/aikit export
- **Date**: 2026-11-01
- **Status**: Accepted
- **Context**: The initial brief builder destroyed uppercase acronyms (REST, API, OAuth2) via naive capitalization, generated static generic milestones regardless of goal context, had a narrow 5-term risk taxonomy, and lacked stdin pipe streaming or markdown/AIKit plan exports.
- **Decision**: Preserve casing of all words while capitalizing the initial character of the first word; expand risk taxonomy to 10 core engineering vectors with keyword aliases; tailor the 4 delivery milestones dynamically to detected domains; support stdin piping via `-` or redirected input; add `--markdown` for GitHub Flavored Markdown brief rendering; and provide `--aikit` to synthesize runnable AIKit checkpoint commands.
- **Consequences**: Existing tests continue to pass with backward-compatible Brief dict representations; brief outputs become significantly more actionable and integrated with AIKit workflows; requires 0 external dependencies (Python standard library only).
