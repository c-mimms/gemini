# Recurring Task: Advanced Software Engineering Job Search (Edinburgh)

## Goal
The goal of this task is to intelligently filter new software engineering job opportunities in Edinburgh based on specific criteria and notify Chris about any good fits.

## Data & Log Files
- **Job Database**: A local file at `/Users/chris/code/gemini/job_agent/scripts/job_database.json` will be used to store structured data for every job that is processed. This prevents re-processing and allows for future analysis.
- **Log File**: A simple log at `/Users/chris/code/gemini/job_agent/scripts/seen_emails.log` will store the message IDs of emails that have already been processed, to avoid re-reading old emails.

## Filtering Criteria
A job is considered a "good fit" if it meets ALL of the following conditions:
1.  **Full-Time**: The job description does not contain keywords like "part-time", "contract", "internship", or "temporary".
2.  **Salary**: The stated salary is greater than £80,000 GBP per year. If no salary is listed, this condition is not met.
3.  **Visa Sponsorship**: EITHER the job description explicitly mentions "visa sponsorship" OR the company is considered "large".
    -   A **large company** is defined as a company that is publicly traded on a major stock exchange (e.g., FTSE, NASDAQ, NYSE) OR has more than 1,000 employees listed on their LinkedIn page.

## Workflow

1.  **Log Start**: Print a message indicating the task has started.
2.  **Read New Emails**:
    -   Print a message: "Reading new emails..."
    -   Use `python /Users/chris/code/gemini/job_agent/scripts/read_email.py` to check for recent, unread emails with subjects related to "New jobs for you in Edinburgh".
    -   For each email found, check its ID against `seen_emails.log`. If already processed, print "Skipping already processed email" and skip it.
    -   Print how many new emails were found. **CRITICAL: If 0 new, unprocessed emails are found, IMMEDIATELY skip to Step 9 (Log Completion). Do not proceed to Step 3.**

3.  **Extract Job URLs**:
    -   Print a message: "Extracting job URLs from emails..."
    -   From the body of each new email, extract all the direct hyperlinks to job postings on LinkedIn.
    -   Print how many URLs were extracted in total. **If 0 URLs were extracted, skip to Step 9.**

4.  **Process Each Job URL**:
    -   For each new URL, check if it already exists in the `job_database.json`. If so, print "Skipping already processed job" and skip it.
    -   If the job is new, use the `browser_use` tool to navigate to the URL. Print "Scraping job details for: [URL]".

5.  **Scrape Job Details**:
    -   On the job page, use `browser_use` with the `eval` command and JavaScript selectors to scrape the following information:
        -   Job Title, Company Name, the full job description text, the salary, and a link to the company's own LinkedIn page.
    -   Print a confirmation message after scraping is complete.

6.  **Scrape Company Details**:
    -   Navigate to the company's LinkedIn page using `browser-use`.
    -   Scrape the number of employees. Print "Found X employees for [Company Name]".

7.  **Filter and Analyze**:
    -   Print "Applying filters to [Job Title]...".
    -   Apply the **Filtering Criteria** to the scraped data.
    -   Use your web search capabilities to check if the company is publicly traded if needed.
    -   Print whether the job was determined to be a "good fit" or not.

8.  **Take Action**:
    -   **For ALL new jobs**: Save the scraped details to `job_database.json`.
    -   **If a job IS a good fit**:
        -   Format and send the summary email using `python /Users/chris/code/gemini/job_agent/scripts/send_email.py`.
        -   Print "Sent notification email for [Job Title]".
    -   **Finally**: Append the message ID of the email to `seen_emails.log`.
9.  **Log Completion**: Print a message indicating the task has finished successfully.
