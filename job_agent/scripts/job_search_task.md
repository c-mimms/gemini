# Recurring Task: Daily Software Engineering Job Search Links

## Goal
The goal of this task is to find pre-filtered links to major job boards for software engineering roles and email them to `christek13@gmail.com`. This task should run every weekday morning.

## Workflow

1.  **Search for Job Board Links**:
    -   Perform a web search using the `google_web_search` tool to find links to job boards.
    -   The query should be something like: `"Software Engineer" jobs in "SF Bay Area" posted in last 7 days on LinkedIn and Indeed`.
    -   The goal is to get the direct URLs to the search results pages on these sites.

2.  **Format the Email**:
    -   If search results are found, create an HTML-formatted email.
    -   The subject should be: "Your Daily Software Engineering Job Links"
    -   The body should start with a heading like `<h1>Today's Job Search Links</h1>` and a short introductory sentence.
    -   Each link found should be a list item (`<li>`) containing a hyperlink (`<a>`) to the job board URL.

3.  **Send the Email**:
    -   Use the `send_email.py` tool to send the HTML email to `christek13@gmail.com`.
    -   Ensure you use the `--html` flag.
    -   If no links are found, do not send an email.
