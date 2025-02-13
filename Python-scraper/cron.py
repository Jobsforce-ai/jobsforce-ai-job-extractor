from flask import Flask, jsonify
import os
from flask_cors import CORS
import math
from jobspy import scrape_jobs
from datetime import datetime, timedelta
from pymongo import MongoClient
from models import insert_job
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
import pytz  # Import pytz for timezone support
load_dotenv()
app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGO_URI")


try:
    client = MongoClient(MONGO_URI)
    db = client['job_database']
    collection = db['jobs']
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f" MongoDB Connection Failed: {e}")

# Set timezone to Eastern Time
eastern_tz = pytz.timezone("America/New_York")

def scrape_and_store_jobs():
    """ Function to scrape jobs, store them in MongoDB, and delete old jobs """
    try:
        print(f"Running job scraper at {datetime.now(eastern_tz).strftime('%Y-%m-%d %H:%M:%S %Z')}...")

        jobs = scrape_jobs(
            site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"],
            search_term="Software Engineer",
            location="USA",
            results_wanted=1000,
            hours_old=24,
            country_indeed="USA"
        )

        if jobs.empty:
            print("No jobs fetched!")
            return

        print(f"Total jobs fetched: {len(jobs)}")

        jobs_dict = jobs.to_dict(orient="records")
        jobs_with_description = [job for job in jobs_dict if job.get('description')]

        print(f"Jobs after filtering descriptions: {len(jobs_with_description)}")

        if jobs_with_description:
            for job in jobs_with_description:
                job['createdAt'] = datetime.utcnow()  # Store UTC time for consistency
                insert_job(job)

            print("Jobs successfully stored in MongoDB.")

        # Delete jobs older than 24 hours
        cutoff_time = datetime.utcnow() - timedelta(hours=24)
        deleted_jobs = collection.delete_many({"createdAt": {"$lt": cutoff_time}})
        print(f"Deleted {deleted_jobs.deleted_count} old jobs.")

    except Exception as e:
        print(f"Error occurred: {e}")

# Initialize the scheduler
scheduler = BackgroundScheduler(timezone=eastern_tz)

# Schedule the job to run every day at 1 AM Eastern Time
scheduler.add_job(scrape_and_store_jobs, "cron", hour=1, minute=0)

# Start the scheduler
scheduler.start()

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    """ API to return jobs from MongoDB """
    try:
        jobs = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB ID field
        return jsonify(jobs)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server on port 5000...")
    scrape_and_store_jobs()  # Run scraper once on startup
    app.run(port=5000, debug=True)
