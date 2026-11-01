# Capability Showcase

[![Built with AIKit](https://img.shields.io/badge/built%20with-AIKit-6f42c1)](https://github.com/AegeanWorks/AIKit)

A polished local-first showcase that demonstrates AI-assisted planning, implementation, testing, and resilient CLI design.

## ⚡ 30-Second Cold-Start Quick Reference

- **Runtime Prerequisites**: Python 3.10+; standard library only.
- **Canonical Regression Shield Gate**:
  ```bash
  python -m unittest discover -s tests -p "test_*.py"
  ```

### ▶️ Try the capability

From this directory:

```bash
python signal_garden.py "ship an auth service"
python signal_garden.py "build a local notes app" --json
python signal_garden.py "deploy payment microservice" --markdown
python signal_garden.py "harden auth layer" --aikit --task-id "auth-v1"
```

Pipe mode from standard input:

```bash
echo "build offline analytics pipeline" | python signal_garden.py -
```

The output is deterministic and local-only: an acronym-safe title, bounded domain-tailored milestones, keyword-based risk prompts across 10 engineering domains, and an effort hint. It is intentionally small so an agent can inspect, test, and extend it quickly.

### 🛠️ AIKit Commands (run from the AIKit folder)
| Role | Command |
|---|---|
| Status, task and gates | `python aikit.py status capability-showcase` |
| Phase 4: every gate | `python aikit.py check capability-showcase` |
| Repair memory and map, then check | `python aikit.py fix capability-showcase` |
| Resume an interrupted task | `python aikit.py resume capability-showcase` |

## 📦 What's Inside

```text
capability-showcase/
├── .gitignore                <- transient AIKit state excluded
├── LICENSE                   <- Aegean License 1.1 (AL-1.1): free personal use
├── COMMERCIAL.md             <- Commercial licensing terms
├── LICENSES/                 <- REUSE license texts
├── REUSE.toml                <- Machine-readable SPDX metadata
├── README.md
├── assets/                   <- brand logo and social preview
├── signal_garden.py          <- dependency-free CLI and brief builder
├── tests/
│   └── test_signal_garden.py
└── .aikit/                   <- this project's memory: record, ledger, decisions
```

## 📜 License

Free for personal use under the Aegean License 1.1 (AL-1.1); see [LICENSE](LICENSE). Any commercial use needs the Aegean Commercial License 1.0 (ACL-1.0); see [COMMERCIAL.md](COMMERCIAL.md).
