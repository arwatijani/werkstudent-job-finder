import sqlite3

DB_NAME = "jobs.db"


def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT,
                location TEXT,
                url TEXT NOT NULL UNIQUE,
                status TEXT NOT NULL DEFAULT 'new'
            )
            """
        )


def save_jobs(jobs):
    added = 0
    with get_connection() as connection:
        for job in jobs:
            cursor = connection.execute(
                "INSERT OR IGNORE INTO jobs (title, company, location, url) "
                "VALUES (?, ?, ?, ?)",
                (
                    job.get("title"),
                    job.get("company_name"),
                    job.get("location"),
                    job.get("url"),
                ),
            )
            added += cursor.rowcount
    return added


def get_jobs(search="", status=""):
    query = "SELECT * FROM jobs WHERE 1=1"
    params = []
    if search:
        query += " AND (title LIKE ? OR company LIKE ? OR location LIKE ?)"
        like = f"%{search}%"
        params.extend([like, like, like])
    if status:
        query += " AND status = ?"
        params.append(status)
    query += " ORDER BY id DESC"
    with get_connection() as connection:
        return connection.execute(query, params).fetchall()


def update_status(job_id, status):
    with get_connection() as connection:
        connection.execute(
            "UPDATE jobs SET status = ? WHERE id = ?", (status, job_id)
        )
