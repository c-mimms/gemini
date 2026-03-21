---
name: git-github
description: Automate common git operations and GitHub interactions using the git and gh CLIs. Use for version control, branching, committing, pushing, and managing PRs/issues.
---

# Git & GitHub Skill

This skill provides guidelines and commands for interacting with Git repositories and GitHub using the `git` and `gh` command-line tools. It should be used to manage version control and repository interactions.

## Continuous Integration (USER RULE)
**Always commit and push any meaningful code change, refactor, or documentation update immediately upon completion and verification.** Ensure the repository stays in sync with the remote at all times.

## 1. Local Git Operations

### Branching & Syncing
- **Create and switch to a new branch**: `git checkout -b <branch-name>`
- **Switch to an existing branch**: `git checkout <branch-name>`
- **Fetch latest from remote**: `git fetch origin`
- **Pull latest changes**: `git pull origin <branch-name>`
- **View current branch and status**: `git status`

### Committing Changes
Ensure commit messages are descriptive.
- **Stage all changes**: `git add .`
- **Stage specific files**: `git add <file1> <file2>`
- **Stage chunks of code**: `git add -p <file>`
- **Commit changes**: `git commit -m "Descriptive commit message"`
- **Amend the last commit** (if not pushed): `git commit --amend -m "New message"`

### Pushing Changes
- **Push a new branch**: `git push -u origin <branch-name>`
- **Push updates to an existing branch**: `git push`

---

## 2. GitHub CLI (`gh`) Operations

The GitHub CLI allows you to interact with GitHub seamlessly from the command line.

### Pull Requests
- **Create a Pull Request**:
  ```bash
  gh pr create --title "Your PR Title" --body "Detailed description of changes"
  ```
- **List open PRs**: `gh pr list`
- **View a specific PR**: `gh pr view <number>`
- **Checkout a PR locally to test/review**: `gh pr checkout <number>`
- **Merge a PR**: `gh pr merge <number> --merge` (or `--squash`, `--rebase`)

### Issues
- **Create an Issue**:
  ```bash
  gh issue create --title "Issue Title" --body "Detailed issue description"
  ```
- **List all open issues**: `gh issue list`
- **View an Issue**: `gh issue view <number>`
- **Close an Issue**: `gh issue close <number>`

### GitHub Actions (Workflows)
- **List recent workflow runs**: `gh run list`
- **View a specific workflow run details and logs**: `gh run view <run-id>`
- **Watch a workflow in progress**: `gh run watch <run-id>`
- **Manually trigger a workflow**: `gh workflow run <workflow-name.yml>`

## Useful Tips
- If there are merge conflicts during a pull, resolve them by editing the files, staging them with `git add`, and running `git commit`.
- Avoid force pushing (`git push -f`) unless absolutely necessary.
