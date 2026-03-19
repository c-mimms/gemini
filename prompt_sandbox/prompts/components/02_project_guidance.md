# Project Guidance, Deployment & System Management

## Repository & Project Structure
- **Root Repository:** The root directory is NOT a git project. All `.git` folders and remote configurations must be managed at the subdirectory level.
- **Project Isolation:** Every new project, website, or application must be created in its own subdirectory. Each project should be fully self-contained unless explicitly requested otherwise. The `dashboard` and `discord_bot` projects are special operational projects for the bot and should not be used as backend for other projects.
- **Per-Project Git:** Each subdirectory must be initialized as its own independent git repository and pushed to GitHub.
- **Documentation & Deployment:** Every project must include a `README.md` and a `terraform/` directory for AWS deployment.

## Deployment & Release Workflow
- **Default for New Requests:** Assume every request for a new feature or site is a NEW project in a NEW subdirectory unless explicitly specified otherwise. If ambiguous, ask for clarification.
- **Versioning:** Use Semantic Versioning (SemVer) for all projects.
- **Commit & Tag:** Before any deployment to AWS, all changes must be committed to the project's local git repository.
- **Releases:** A release tag (e.g., `v1.0.0`) must be cut (git tag) for every deployment. The first deployment should always be tagged `v1.0.0`.
- **Registry:** Every new deployment, deletion, or status change MUST be recorded in the root `registry.json` file. This is the bot's single source of truth for all projects, URLs, and IPs.

## System Management & Agent Lifecycle
- **Cleanup:** Explicitly track and `kill` PIDs of any background processes spawned during testing or execution. Use `pkill` with specific filters only when certain that no system/Antigravity processes will be affected.
- **Persistence:** You may spawn long-lived processes (e.g., servers, dashboards) that should persist after your turn ends.
- **Tracking:** ALL semi-permanent PIDs MUST be appended to `.gemini_pids` in the project root for tracking and easy manual cleanup. 
- **Log Format:** Each entry must follow this format: `[TIMESTAMP] PID - COMMAND - RATIONALE`. 
- **Status Management:** When a process is intentionally stopped or confirmed dead, prefix the line with `[TERMINATED]`.
- **Survival:** Use `nohup` and `&` to ensure processes survive the session.
- **Safety**: Before spawning any new process, scan `.gemini_pids` and verify the required ports/resources are free. If a conflict is detected, identify the existing PID and propose a shutdown or migration plan to the user.
