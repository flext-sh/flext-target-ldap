# AGENTS.md — flext-target-ldap

> **Parent workspace law** lives in [`../AGENTS.md`](../AGENTS.md) — read it first.
> Universal engineering core: `~/.agents/UNIVERSAL_CORE.md`. Composition: global
> skills + parent/root `AGENTS.md` + this scope delta. Do not re-embed universal law.
>
> **Standalone / independent mode:** when `../AGENTS.md` does not resolve, pin the
> parent raw `AGENTS.md` URL to the same branch/release as this package (never
> `main`): <https://raw.githubusercontent.com/flext-sh/flext/0.12.0-dev/AGENTS.md>

<!-- AIHUB-AGENTS-SCOPE-LOCAL-BEGIN -->

**Package:** `flext_target_ldap` · deps: `flext-cli`, `flext-core`, `flext-ldap`,
`flext-meltano`

## Overview

Singer **target** (loader) for LDAP directory loading. Thin driver over `flext-meltano`
(ADR-006, amended 2026-10-25): `FlextTargetLdap` subclasses
`FlextMeltanoTargetServiceBase` and declares only `target_name` and `sink_factory`.
Writes are delegated to `flext-ldap` through an injected directory capability.

## Structure

```text
src/flext_target_ldap/
├── api.py               # FlextTargetLdap: composition root (target_name, sink_factory)
├── cli.py               # console entry point: main() -> FlextTargetLdap().cli_main()
├── config/target-ldap.yaml   # stream entry profiles (business rules)
├── services/client.py   # FlextTargetLdapClient: concrete flext-ldap directory adapter
├── services/sinks.py    # FlextTargetLdapSinks: one profile-driven sink + create_sink
├── constants.py typings.py protocols.py models.py utilities.py   # AUTO-GENERATED
└── _constants/ _models/ _protocols/ _typings/ _utilities/
```

## Code Map

| Symbol                            | Kind  | Location                | Role                                                 |
| --------------------------------- | ----- | ----------------------- | ---------------------------------------------------- |
| `FlextTargetLdap`                 | class | `api.py`                | binds `sink_factory` and the concrete directory      |
| `FlextTargetLdapSinks`            | class | `services/sinks.py`     | profile-driven stream sink and `create_sink`         |
| `FlextTargetLdapClient`           | class | `services/client.py`    | add, modify, delete, search through `flext-ldap`     |
| `p.TargetLdap.Directory`          | proto | `_protocols/base.py`    | the add/modify/delete capability a sink consumes     |
| `FlextTargetLdapUtilitiesEntries` | class | `_utilities/entries.py` | stateless `u.TargetLdap` profile and entry mapping   |
| `main`                            | code  | `cli.py`                | the single console entry point                       |

## Singer contract

- stdin is routed only by `u.Meltano.process_stdin` through the base `cli_main`.
  The target owns no message parsing.
- SCHEMA registers the stream sink built by `sink_factory`.
- One sink class serves every stream. The stream's entry profile in
  `config/target-ldap.yaml` declares its RDN attribute, identity fields, object
  classes and field mapping; a stream without a declared profile uses the declared
  default profile.
- RECORD is written immediately: an explicit `dn` wins, otherwise the DN is derived
  from the profile. The sink adds the entry, modifies it when the DN was already
  written in this run, and deletes it when `_sdc_deleted_at` is set. When an add fails
  and `update_existing_entries` is true, the sink modifies the entry; any other
  failure fails the record.
- STATE flushes every registered sink.

### Failure behavior (changed 2026-10-25, bead `flext-pawp5`)

- A RECORD without `stream` fails validation; there is no stream default.
- A line that is not valid JSON fails; a RECORD whose `record` is not a mapping fails.
- Blank lines and JSON lines that are not objects are skipped by the `flext-meltano`
  router, not by this target.
- Failures surface as `r.fail` through the base drain, and `cli_main` exits with
  status 1.
- The console script reads no configuration-file argument: the base `cli_main` ignores
  its arguments, and `sink_factory` receives the service `settings_overrides`.

## Anti-Patterns / Gotchas

- **`api.py` is a pure MRO facade** (ADR-028): no method or function definitions.
  Stateful behavior belongs in `services/`; stateless behavior belongs in
  `u.TargetLdap` (`_utilities/`, static methods only).
- **Directory access is injected, never looked up** (operator order 2026-10-25,
  tracker key `operator-order-2026-10-25-servers-di-never-registry`). Sinks and `u`
  consume `p.TargetLdap.Directory` and never name a concrete client, server, or
  registry. `api.py` is the only place that binds `FlextTargetLdapClient`.
- **No stream-to-class registry.** Stream behavior is data in
  `config/target-ldap.yaml`; adding a stream adds a profile, never a sink class.

### ADR-028 Decision 16: CA/DI and quality

The injected `p.TargetLdap.Directory` and the `api.py` composition root above are this
member's declaration for [FLEXT ADR-028 Decision 16](https://github.com/flext-sh/flext/blob/0.12.0-dev/docs/architecture/adr/028-facade-boundary-orchestrators-declarative-enforcement.md#decision-16).
Current implementation and gate evidence is tracked in Bead `flext-pawp5`.

## Conventions (specific to this package)

- Config/settings canonical pattern: ADR-005 (SSOT) and ADR-024 (DI config contract).
- Codemod governance (ast-grep + make mod): ADR-014.

## Commands

Run standard verbs from the active workspace root without project or file selectors:

```bash
make setup
make check
make tests
```

<!-- AIHUB-AGENTS-SCOPE-LOCAL-END -->

<!-- AIHUB-GOVERNANCE-INSTRUCTIONS-BEGIN -->
<!-- AIHUB-GOVERNANCE-CAPSULE v1 sha256:5888ee9f8147f63364a4f7cd6906e9d837f58cb8a8546844760c526ecb1a303b -->

# Generated session governance capsule

This projection is derived by `agentsctl sync`; edit canonical `AGENTS.md`, `rules/`,
`skills/`, or `commands/`, never this output. The operator's newest request has
precedence. Provider hooks are delivery mechanisms, not policy owners.

## Rule `architecture/engineering-core`

# Engineering core

For every implementation:

1. Research repository owners, dependencies, and canonical documentation.
2. Remove scope without a current requirement or consumer (YAGNI).
3. Elect one writable authority; every other copy is a generated projection (SSOT).
4. Apply SOLID only to a responsibility or dependency boundary under change.
5. Implement through the owner and simplify without weakening behavior.
6. Remove duplication and god components; recheck YAGNI, SSOT, SOLID.
7. Exercise runtime behavior, run every applicable native gate, and complete the
   approved landing cycle before changing phase.

At a cross-boundary failure, prove the producer contract and output. Fix its owner when
invalid or the receiver when it conforms. Never alter a correct adjacent owner for an
invalid consumer; symptom workarounds are defects.

Hardcodes, normalized failure, failover, retry, fallback, compatibility, partial
execution, keyring, and unevidenced success are defects. Typed owners keep defaults. The
first exception escapes its CLI with traceback and cause.

Git, runtime, build, and tests are baseline. Auxiliary tracking is a capability.
Auxiliary capabilities apply only when authorized and selected; installation never
selects. Do not load, probe, or gate dormant capabilities. Invalid selected
authorization, configuration, readiness, or result fails without fallback. Require only
non-derivable values.

An external token validation without its token is not executed and is recorded as
`NOT EXECUTED`, never green; it does not block offline gates, landing, or post-merge
proof. Direct invocation selects it: the token becomes required and any failure escapes
without skip, catch, fallback, or normalization.

Compose with `generalized ownership` (rule file), `strict execution` (rule file),
`runtime evidence` (rule file), `storage isolation` (rule file), `security closure`
(rule file).

## Rule `coordination/operator-precedence`

# Newest operator instruction wins; adjust artifacts to it

Authority order: operator request > declared orchestration contract > canonical
tracker > ADRs > skills > docs, and newest supersedes oldest. On conflict, adjust the
lower or older artifact to match; never override the operator to satisfy stale guidance.

While orchestration and tracker runtimes are suspended, do not invoke them. Create no
substitute tracker or ledger, preserve implementation evidence only in separately
authorized Git/PR/CI, and leave phase closure open.

Exact operator authorization naming targets, disposition, recovery, and validation
survives interruption, divergence, and red gates; re-preflight and continue. Ask only
when the effect expands beyond it or two evidenced current intentions conflict. State
alone proves no intention, actor, or process.

## Rule `ethics/professional-integrity`

# Professional integrity is absolute

Never lie, fabricate evidence, hide a blocker, bypass a gate, or patch a symptom only to
make a check pass. Fix the generalized root cause with full context and report exact
command, working directory, exit code and decisive output.

## Rule `runtime/strict-execution`

# Strict execution is universal and non-optional

Every project and projected agent applies all of these policies together:

- `fail loud` (rule file);
- `no fallback` (rule file);
- `preflight before effects` (rule file);
- `required environment` (rule file);
- `atomic effects` (rule file);
- `causal subprocess propagation` (rule file);
- `no keyring` (rule file);
- `zero residue` (rule file).

The policies are cumulative. A project rule may make them narrower or reject more
inputs; it cannot relax, catch, normalize, skip, defer, or route around any of them.
Existing opposing behavior is a blocking violation to exterminate at its owner, never
grandfathered compatibility.

Resolve gate applicability before invocation. A dormant external-token gate is not
executed; selecting or invoking it applies every policy above.

## Capability indexes

Skills: caveman, context-canary, fix-forward-collaboration, governance-audit,
operator-correction-learning, plan-focus-recovery, sprint-closure, strategic-compact,
verification-loop Commands: add-language-rules, database-migration, feature-development,
ghi-list, pr-list, ralph-loop, security-triage, synthesize-governance

<!-- AIHUB-GOVERNANCE-INSTRUCTIONS-END -->

<!-- BEGIN BEADS INTEGRATION v:1 profile:minimal hash:970c3bf2 -->

## Beads Issue Tracker

This project uses **bd (beads)** for issue tracking. Run `bd prime` to see full workflow
context and commands.

### Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --claim  # Claim work
bd close <id>         # Complete work
```

### Rules

- Use `bd` for ALL task tracking — do NOT use TodoWrite, TaskCreate, or markdown TODO
  lists
- Run `bd prime` for detailed command reference and session close protocol
- Use `bd remember` for persistent knowledge — do NOT use MEMORY.md files

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data`
on your git remote; `.beads/issues.jsonl` is a passive export. See
<https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md> for details and
anti-patterns.

## Agent Context Profiles

The managed Beads block is task-tracking guidance, not permission to override
repository, user, or orchestrator instructions.

- **Conservative (default)**: Use `bd` for task tracking. Do not run git commits, git
  pushes, or Dolt remote sync unless explicitly asked. At handoff, report changed files,
  validation, and suggested next commands.
- **Minimal**: Keep tool instruction files as pointers to `bd prime`; use the same
  conservative git policy unless active instructions say otherwise.
- **Team-maintainer**: Only when the repository explicitly opts in, agents may close
  beads, run quality gates, commit, and push as part of session close. A current "do not
  commit" or "do not push" instruction still wins.

## Session Completion

This protocol applies when ending a Beads implementation workflow. It is subordinate to
explicit user, repository, and orchestrator instructions.

1. **File issues for remaining work** - Create beads for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **Handle git/sync by active profile**:

   ```bash
   # Conservative/minimal/default: report status and proposed commands; wait for approval.
   git status
   
   # Team-maintainer opt-in only, unless current instructions forbid it:
   git pull --rebase
   bd dolt push
   git push
   git status
   ```

5. **Hand off** - Summarize changes, validation, issue status, and any blocked
   sync/commit/push step

**Critical rules:**

- Explicit user or orchestrator instructions override this Beads block.
- Do not commit or push without clear authority from the active profile or the current
  user request.
- If a required sync or push is blocked, stop and report the exact command and error.

<!-- END BEADS INTEGRATION -->

<!-- BEGIN BEADS CODEX SETUP: generated by bd setup codex -->

## Beads Issue Tracker

Use Beads (`bd`) for durable task tracking in repositories that include it. Use the
`beads` skill at `.agents/skills/beads/SKILL.md` (project install) or
`~/.agents/skills/beads/SKILL.md` (global install) for Beads workflow guidance, then use
the `bd` CLI for issue operations.

### Quick Reference

```bash
bd ready                # Find available work
bd show <id>            # View issue details
bd update <id> --claim  # Claim work
bd close <id>           # Complete work
bd prime                # Refresh Beads context
```

### Rules

- Use `bd` for all task tracking; do not create markdown TODO lists.
- Run `bd prime` when Beads context is missing or stale. Codex 0.129.0+ can load Beads
  context automatically through native hooks; use `/hooks` to inspect or toggle them.
- Keep persistent project memory in Beads via `bd remember`; do not create ad hoc memory
  files.

**Architecture in one line:** issues live in a local Dolt DB; sync uses `refs/dolt/data`
on your git remote; `.beads/issues.jsonl` is a passive export. See
<https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md> for details and
anti-patterns.

<!-- END BEADS CODEX SETUP -->
