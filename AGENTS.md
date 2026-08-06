# AGENTS.md — flext-target-ldap

> **Parent workspace law** lives in [`../AGENTS.md`](../AGENTS.md) — read it first.
> Universal engineering core: `~/.agents/UNIVERSAL_CORE.md`. Composition: global skills + parent/root `AGENTS.md` + this scope delta. Do not re-embed universal law.
>
> **Standalone / independent mode:** when `../AGENTS.md` does not resolve, pin the parent raw `AGENTS.md` URL to the same branch/release as this package (never `main`).

<!-- AIHUB-AGENTS-SCOPE-LOCAL-BEGIN -->
**Package:** `flext_target_ldap` · deps: `flext-cli`, `flext-core`, `flext-ldap`, `flext-meltano`

## Overview

Singer **target** (loader) for LDAP directory loading. Thin driver over `flext-meltano` (ADR-006), delegating writes to `flext-ldap`.

## Structure

```text
src/flext_target_ldap/
├── api.py            # FlextTargetLdap (public implementation)
├── target.py         # CLI compatibility wrapper → FlextTargetLdap.run_cli()
├── singer/ application/ patterns/   # supporting domain modules
├── constants.py typings.py protocols.py models.py utilities.py   # AUTO-GENERATED facets
└── _constants/ _models/ _utilities/
```

## Code Map

| Symbol | Kind | Location | Role |
|--------|------|----------|------|
| `FlextTargetLdap` | class | `api.py` | public loader; uses meltano target abstractions |
| CLI wrapper | code | `target.py` | `run_cli()` only |

## Anti-Patterns / Gotchas

- **`target.py` is a compatibility entrypoint only** — do not add behavior there; the implementation is in `api.py` + `singer/`/`application/`/`patterns/`.

## Conventions (specific to this package)

- Config/settings canonical pattern: ADR-012.
- Codemod governance (ast-grep + make mod): ADR-014.

## Commands

```bash
make check PROJECT=flext-target-ldap
make test  PROJECT=flext-target-ldap       # tests/unit
```
<!-- AIHUB-AGENTS-SCOPE-LOCAL-END -->
