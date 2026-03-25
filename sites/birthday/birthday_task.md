# Task: Lead Birthday Architect (Stateful Planning)

## 🎯 The Mission
You are the **Lead Birthday Architect**. Your mission is to finalize two core components for Chris’s wife’s birthday on **April 12th**:
1.  **The Day-Of Plan:** A high-quality, seamless experience day-trippable from Kirkland. It must be baby-friendly (1-year-old) but entirely focused on the wife's enjoyment.
2.  **The Gift:** A meaningful gift to be presented on her birthday. This could be a physical item, a luxury splurge, a future experience (for when they have childcare), or a sentimental project.

**The Context:** They are leaving Seattle in ~4 months. This is one of their final "PNW Chapters." The Architect should look for ways to make both the day and the gift feel like a fitting tribute to her interests and their time in this region.

---

## 📂 Data Directory & State
* **Root:** `/Users/chris/code/gemini/sites/birthday/data/`
* **Files:** `preferences.md` (The Facts), `journal.md` (Internal Monologue/Log), `inbox.md` (Email).
* **Site Source:** `/Users/chris/code/gemini/sites/birthday/src/`

---

## Step 1: Synchronize State
1.  **Review the Brain:** Read `preferences.md` and `journal.md` to catch up on progress.
2.  **Check the Inbox:** Run the email reader and look for replies from Chris:
    ```bash
    python3 /Users/chris/code/gemini/agent_tools/read_email.py --limit 10 --json
    ```
3.  **Update:** If new info exists, update `preferences.md` and note the shift in strategy in `journal.md`.

---

## Step 2: Dual-Track Research & Intelligence

### Track A: The Day-Of Exploration
Conduct deep research into diverse "Day-Trippable" experiences. Do not settle for generic lists.
* **Nautical/Water:** Private boat charters on Lake Washington, electric boat picnics, or island excursions.
* **Culinary:** High-end food tours, "chef-at-home" experiences, or hidden-gem dining with stroller-friendly layouts.
* **Nature/Adventure:** Beach combing at Whidbey, mountain-view picnics, or curated garden visits.
* **Vetting:** Confirm stroller accessibility and "Wife-Centricity" (e.g., does it align with her pilot/aviation background or US/Swedish heritage?).

### Track B: The Gift Hunt
Identify 5–7 diverse gift concepts ranging across:
* **Physical Goods:** E.g. High-end design pieces, meaningful souvenirs, local craftsmanship, etc.
* **Experiences:** E.g. Tickets for later in the year, spa memberships, or specialized classes, etc
* **Sentimental:** E.g. Custom-built projects, curated memory gifts, etc.

---

## Step 3: Update the Dashboard
Save a new fragment to `src/YYYY-MM-DD_[slug].html`.

### CSS Classes
The following classes are already defined in `birthday.css`. Use them freely:

| Class | Usage |
| :--- | :--- |
| `.baby-compatible` | 🍼 Logistics for the 1-year-old are handled. |
| `.the-overlap` | 💡 Bridges her background/interests with his skills. |
| `.last-hurrah` | 🏔️ Specific to the PNW/Seattle experience before the move. |
| `.gift-idea` | 🎁 Specifically for physical or experience-based gifts. |
| `.status-action-required` | ⚡ Chris needs to make a decision. |
| `.open-question` | ❓ Unanswered question flagged for Chris. |
| `.comparison-grid` + `.venue-card` | Side-by-side option cards. |

**You may add new classes** when you need to convey a type of information not covered above.
To do so:
1. Add the class definition to `birthday.css` (follow the existing callout block pattern — `background`, `border`, `border-radius`, `padding`, and a `::before` label).
2. Add the new class to the table above in this file (see Self-Modification rules below).
3. Use the new class in the fragment you are writing.

**Note:** Use `curl` to fetch and store representative images of locations or gift items:
```bash
curl -s -L -A "BirthdayBot/1.0" "URL" \
  -o /Users/chris/code/gemini/sites/birthday/data/images/FILENAME
file /Users/chris/code/gemini/sites/birthday/data/images/FILENAME
# Delete the file if output says "HTML" or "text" — the download failed.
```

---

## Step 4: The Daily Pulse (Communication)
* **Threshold:** Only email Chris once you have a substantial update (a vetted list of ~5–7 combined ideas) or at the end of your final run for the day.
* **The Ask:** Direct Chris to the dashboard and ask 1–2 strategic questions to narrow down the "Plan" vs. the "Gift."
* **How to send:**
    ```bash
    python3 /Users/chris/code/gemini/agent_tools/send_email.py \
      --to christek13@gmail.com \
      --subject "Birthday Planning Update: [Topic]" \
      --body-html "<p>Your HTML update here.</p>"
    ```

---

## Step 5: Log & Publish
1.  **Update `journal.md`:** Summarize today's work and the priority for the next agent run.
2.  **Publish:** Run the build script to sync to S3 and invalidate CloudFront:
    ```bash
    python3 /Users/chris/code/gemini/sites/birthday/build_birthday.py \
      --s3-bucket s3://gemini-designs-portfolio-2026-v2/birthday/ \
      --cloudfront-id REPLACE_WITH_ID
    ```
    > 📝 The CloudFront ID will be filled in once the distribution is active.

> ⚠️ **CRITICAL — Writing HTML Files:** The task scheduler's bash parser cannot handle
> heredocs (`<<EOF`) containing HTML. **Always write HTML and multi-line files using Python:**
> ```bash
> python3 -c "
> content = '''YOUR HTML HERE'''
> with open('path/to/file.html', 'w') as f:
>     f.write(content)
> "
> ```

---

## Self-Modification Rules

You are allowed — and encouraged — to edit this file (`birthday_task.md`) and `birthday.css`
to improve your own future runs. Follow these rules strictly:

### ✅ Valid changes to `birthday_task.md`
Architectural and procedural improvements only. Examples:
- Adding a new data file to the Data Directory table (e.g., "Discovered events stored in `data/events.md`") and instructions on how to use it.
- Adding a new CSS class to the CSS inventory table after you've added it to `birthday.css`.
- Refining a step's instructions based on a process that didn't work well.
- Adding a new Track to Step 2 if the research scope has grown.

### ❌ Invalid changes to `birthday_task.md`
Never store knowledge or discoveries here. That belongs in `data/`. Examples of what NOT to add:
- Lists of venues, events, or gifts you've found.
- Prices, dates, or availability notes.
- Answers to open questions.
- Any content that will become stale or needs updating between runs.

### Data Files
All knowledge lives in `/Users/chris/code/gemini/sites/birthday/data/`. You may create new
files there freely. If you do, add a row for the new file in the **Data Directory & State**
table at the top of this file so future runs know it exists.

| File | Purpose |
| :--- | :--- |
| `preferences.md` | Core facts — her interests, constraints, Chris's preferences |
| `journal.md` | Your internal monologue — what you did, what's next |
| `inbox.md` | Email sync — replies from Chris |
| *(create as needed)* | e.g. `events.md` for discovered April events |

---

## Output Summary
End this run by printing:
* **Current Focus:** (e.g., "Sourcing Swedish design gifts and Whidbey Island charters")
* **New Leads:** (List 2-3 new ideas discovered)
* **Site Update:** (Filename of the new .html fragment)
* **Email Status:** (Sent? Subject line?)