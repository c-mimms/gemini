#!/bin/bash

# This script sends an email with pre-filtered links to job search websites.

# Directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# The email body with the direct links
EMAIL_BODY="<h1>Today's Job Search Links</h1>
<p>Here are the links to the latest software engineering job postings:</p>
<ul>
  <li><a href=\"https://www.indeed.com/jobs?q=software+engineer&l=San+Francisco+Bay+Area,+CA&fromage=7\">Indeed: Software Engineer, SF Bay Area (Last 7 Days)</a></li>
  <li><a href=\"https://www.linkedin.com/jobs/search/?keywords=Software%20Engineer&location=San%20Francisco%20Bay%20Area&f_TPR=r604800\">LinkedIn: Software Engineer, SF Bay Area (Last 7 Days)</a></li>
</ul>
<p>Best,<br>Chloe</p>"

# Send the email using the send_email.py script
python3 "$SCRIPT_DIR/../bin/send_email.py" --to "christek13@gmail.com" --subject "Your Daily Software Engineering Job Links" --body "$EMAIL_BODY" --html
