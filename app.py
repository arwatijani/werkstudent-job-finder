import requests
from flask import Flask, redirect, render_template, request, url_for

import database
from jobs import fetch_jobs, matches

app = Flask(__name__)

STATUSES = ["new", "applied", "rejected"]


@app.route("/")
def index():
    search = request.args.get("search", "")
    status = request.args.get("status", "")
    jobs = database.get_jobs(search, status)
    return render_template(
        "index.html",
        jobs=jobs,
        search=search,
        status=status,
        statuses=STATUSES,
    )


@app.route("/refresh", methods=["POST"])
def refresh():
    try:
        found = [job for job in fetch_jobs() if matches(job)]
    except requests.RequestException:
        found = []
    database.save_jobs(found)
    return redirect(url_for("index"))


@app.route("/status/<int:job_id>", methods=["POST"])
def change_status(job_id):
    status = request.form.get("status")
    if status in STATUSES:
        database.update_status(job_id, status)
    return redirect(url_for("index"))


if __name__ == "__main__":
    database.init_db()
    app.run(debug=True, port=5001)
