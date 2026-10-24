# Contributing to DearyMe-

We're 3 people, each running a coding agent. That means more branches, more
commits, and bigger diffs than a normal project of this size — so the rules
below exist to keep `main` reviewable, not to slow anyone down.

## Branches

`<your-initials>/<short-description>`, e.g. `jd/notebook-cleanup`,
`ac/data-loader`. Agents will often auto-generate branch names
(`claude/wizardly-allen-o9jhhx`) — rename before pushing, or push to a
renamed branch, so every branch traces back to the human who owns it. Never
push directly to `main`.

## Pull request size

One concern per PR. Target under **~400 changed lines**, excluding
lockfiles, generated files, and notebook output diffs. If your agent
produced a bigger diff, that's a signal to split it: land refactors and
feature changes in separate PRs. Small PRs are non-negotiable here —
agents generate large diffs by default, and a 2,000-line PR from an agent
is nearly impossible for a human to actually review.

## Review

Every PR needs **one human review from someone other than the author**
before merging, even if an agent wrote 100% of the code and it passes CI.
The author is responsible for reading their own agent's diff first —
"the agent wrote it" is not a substitute for the author understanding
what changed. Don't approve your own PR, and don't rubber-stamp a
teammate's just because CI is green.

## What an agent may touch without asking

An agent may freely edit files inside the scope of its assigned task
(the feature/bugfix it was pointed at) and add tests for that work.
It must **stop and ask a human** before it:
- touches CI/workflow config, `CONTRIBUTING.md`, or root-level config files
- adds, removes, or upgrades a dependency
- edits a file outside the directory/module it was told to work in
- rewrites git history or force-pushes a shared branch
- deletes data files or notebooks it didn't create

## Avoiding two agents on the same file

Before starting a task, post in the team channel (or as an issue comment)
which file(s)/directory you're about to work in. Whoever's there first
"owns" that path until their PR merges. Practical rules to make this
painless:
- Keep PRs scoped to one directory where possible — it's the single
  biggest thing that prevents collisions.
- Merge (or close) fast; don't let branches sit for days accumulating
  drift on shared files.
- Rebase onto `main` before opening a PR, not after a conflict appears.
- If you do hit a conflict, the person who merges second resolves it —
  don't ask the first person to redo their work.

## Commit messages

Format: `<type>: <what changed, imperative mood>`, e.g.
`fix: handle empty date field in entry parser`. Types: `feat`, `fix`,
`refactor`, `docs`, `test`, `chore`. One logical change per commit. If an
agent authored the commit, keep the `Co-Authored-By` trailer it adds —
don't strip it. The body should say *why*, not restate the diff.

## Repo structure

Keep new files in the matching top-level folder so agents (and humans)
can predict where things live:

```
/src/        application code, organized by feature/module
/tests/      tests, mirroring the /src/ layout
/notebooks/  exploratory or analysis notebooks (not production code)
/scripts/    one-off or maintenance scripts
/docs/       design notes, architecture decisions
/data/       small sample/fixture data only — never real user data or
             large raw datasets (gitignore these; use external storage)
```

If a task doesn't obviously fit one of these, ask before inventing a new
top-level folder — one-off directories are how repos rot.
