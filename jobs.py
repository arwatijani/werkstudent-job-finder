import csv
import time

import requests

API_URL = "https://www.arbeitnow.com/api/job-board-api"
KEYWORDS = ["werkstudent", "working student"]
LOCATIONS = ["darmstadt", "frankfurt", "mainz", "mannheim"]
TECH_WORDS = [
    "software", "entwickl", "developer", "informatik", "python", "c++",
    "java", "web", "data", "daten", "devops", "cloud", "security",
    "qa", "test", "engineer", "backend", "frontend",
]


def fetch_jobs(pages=5):
    jobs = []
    for page in range(1, pages + 1):
        response = requests.get(API_URL, params={"page": page}, timeout=10)
        response.raise_for_status()
        jobs.extend(response.json().get("data", []))
        time.sleep(1)
    return jobs


def matches(job):
    title = job.get("title", "").lower()
    location = job.get("location", "").lower()
    tags = " ".join(job.get("tags") or []).lower()
    is_student_job = any(word in title for word in KEYWORDS)
    is_nearby = job.get("remote", False) or any(
        city in location for city in LOCATIONS
    )
    is_tech = any(word in f"{title} {tags}" for word in TECH_WORDS)
    return is_student_job and is_nearby and is_tech


def remove_duplicates(jobs):
    unique = {}
    for job in jobs:
        unique[job.get("url")] = job
    return list(unique.values())


def save_to_csv(jobs, filename="jobs.csv"):
    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["title", "company", "location", "url"])
        for job in jobs:
            writer.writerow([
                job.get("title"),
                job.get("company_name"),
                job.get("location"),
                job.get("url"),
            ])


def main():
    jobs = remove_duplicates([job for job in fetch_jobs() if matches(job)])
    print(f"Found {len(jobs)} matching jobs\n")
    for job in jobs:
        print(f"{job.get('title')} - {job.get('company_name')} "
              f"({job.get('location')})")
        print(job.get("url"), "\n")
    save_to_csv(jobs)


if __name__ == "__main__":
    main()
