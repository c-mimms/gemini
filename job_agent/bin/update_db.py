import json
import datetime

db_path = "/Users/chris/code/gemini/job_agent/data/job_database.json"
today = datetime.date.today().isoformat()

with open(db_path, "r") as f:
    db = json.load(f)

# Define known details for specific job IDs
known_jobs = {
    "4354805392": {
        "title": "Senior Software Engineer",
        "company": "Flexera",
        "description": "C#, .NET, JavaScript, React, Angular. Hybrid ITAM and FinOps SaaS.",
        "salary": "Not specified",
        "company_linkedin": "https://www.linkedin.com/company/flexera/",
        "is_good_fit": False
    },
    "4359555180": {
        "title": "Senior Software Engineer, Backend - Distributed Systems",
        "company": "Camunda",
        "description": "Building a durable, highly available streaming platform. Remote-first.",
        "salary": "£90,300 - £148,500",
        "company_linkedin": "https://www.linkedin.com/company/camunda/",
        "is_good_fit": False # No visa/large company match
    },
    "4361313986": {
        "title": "Senior Software Engineer II, Backend - Account Insights",
        "company": "HubSpot",
        "description": "Automating data clean-up and improving data quality at scale. Java, AWS, Kubernetes.",
        "salary": "£84,000 - £126,000 (estimated)",
        "company_linkedin": "https://www.linkedin.com/company/hubspot/",
        "is_good_fit": True
    },
    "4368746703": {
        "title": "SOFTWARE ENGINEERING EXPERT",
        "company": "Great Value Hiring",
        "description": "AI systems improvement, code validation, prompt refinement. Likely contract.",
        "salary": "$50 - $150/hr",
        "company_linkedin": "",
        "is_good_fit": False
    },
    "4377414905": {
        "title": "Principal Developer Technology Engineer",
        "company": "NVIDIA",
        "description": "Advanced rendering (path tracing, neural graphics) and AI adoption in games.",
        "salary": "£80,000 - £120,000 (estimated)",
        "company_linkedin": "https://www.linkedin.com/company/nvidia/",
        "is_good_fit": True
    },
    "4385465666": {
        "title": "Senior Software Engineer",
        "company": "Bright Purple",
        "description": "Generalist software engineer for an R&D tech start-up in Edinburgh. React, Node.",
        "salary": "£60,000 - £75,000",
        "company_linkedin": "",
        "is_good_fit": False
    },
    "4386867460": {
        "title": "Senior Software Engineer",
        "company": "Haystack",
        "description": "High-growth AI scale-up. Ruby on Rails, React, AWS.",
        "salary": "£80,000 - £95,000",
        "company_linkedin": "https://www.linkedin.com/company/wearehaystack",
        "is_good_fit": False
    },
    "4386876313": {
        "title": "SOFTWARE ENGINEER - FULLY REMOTE UK",
        "company": "Haystack",
        "description": "Back-End specialist for high-volume transaction systems. Java, Spring Boot.",
        "salary": "£50,000 - £60,000",
        "company_linkedin": "https://www.linkedin.com/company/wearehaystack",
        "is_good_fit": False
    },
    "4387860626": {
        "title": "Senior Software Engineer",
        "company": "Zumo",
        "description": "Digital Assets Infrastructure team. Node.js, TypeScript, PostgreSQL.",
        "salary": "£75,000",
        "company_linkedin": "https://www.linkedin.com/company/zumo/",
        "is_good_fit": False
    },
    "4388120633": {
        "title": "Software Engineer",
        "company": "Hyra",
        "description": "Java Full Stack Engineer for public services transformation. SC clearance required.",
        "salary": "£45,000 - £75,000",
        "company_linkedin": "https://www.linkedin.com/company/joinhyra",
        "is_good_fit": False
    },
    "4387277344": {
        "title": "Software Engineer (Contract)",
        "company": "Hyra",
        "description": "Secure Government sector project. Full-stack development.",
        "salary": "£550 - £675/day",
        "company_linkedin": "https://www.linkedin.com/company/joinhyra",
        "is_good_fit": False
    }
}

new_urls_file = "/Users/chris/.gemini/tmp/chris/all_new_urls.txt"
with open(new_urls_file, "r") as f:
    for line in f:
        url = line.strip()
        job_id = url.split('/')[-2]
        if job_id in known_jobs:
            details = known_jobs[job_id]
            entry = {
                "url": url,
                "title": details["title"],
                "company": details["company"],
                "description": details["description"],
                "salary": details["salary"],
                "company_linkedin": details["company_linkedin"],
                "is_good_fit": details["is_good_fit"],
                "processed_date": today
            }
        else:
            entry = {
                "url": url,
                "title": "Software Engineer",
                "company": "Unknown",
                "description": "Details could not be scraped.",
                "salary": "Not specified",
                "company_linkedin": "",
                "is_good_fit": False,
                "processed_date": today
            }
        db.append(entry)

with open(db_path, "w") as f:
    json.dump(db, f, indent=2)
