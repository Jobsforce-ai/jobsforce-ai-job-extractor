from flask import Flask, jsonify
import os
from flask_cors import CORS
import math
from jobspy import scrape_jobs
from datetime import datetime
from pymongo import MongoClient
from models import insert_job
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from datetime import datetime, date, timedelta, UTC
import pytz
from config import Config
load_dotenv()
app = Flask(__name__)
CORS(app)

# MONGO_URI = os.getenv("MONGO_URI")
try:
    client = MongoClient(Config.MONGO_URI)
    db = client['job_database']
    collection = db['jobs']
    # Create a unique index to prevent duplicates
    collection.create_index([
        ("job_url", 1),
        ("company", 1),
        ("job_title", 1)
    ], unique=True)
    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f" MongoDB Connection Failed: {e}")

# Set timezone to Eastern Time
eastern_tz = pytz.timezone("America/New_York")

# Function to clean and serialize data
def clean_data(obj):
    if isinstance(obj, (date, datetime)):
        return obj.isoformat()
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    elif isinstance(obj, list):
        return [clean_data(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: clean_data(value) for key, value in obj.items()}
    return obj


# Filter out jobs without descriptions
def filter_jobs_with_description(jobs):
    filtered_jobs = []
    for job in jobs:
        description = job.get('description')
        # Check for None, empty string, NaN, and other falsy values
        if description is not None and description != '' and not (
            isinstance(description, float) and math.isnan(description)
        ):
            filtered_jobs.append(job)
    return filtered_jobs

def scrape_and_store_jobs():
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
        # Use our new filter function
        jobs_with_description = filter_jobs_with_description(jobs_dict)

        print(f"Jobs after filtering descriptions: {len(jobs_with_description)}")

        if jobs_with_description:
            # Use our new clean_data function
            cleaned_jobs = [clean_data(job) for job in jobs_with_description]
            
            # Add creation timestamp
            for job in cleaned_jobs:
                job['createdAt'] = datetime.now(UTC)
            
            # Use insert_many with ordered=False to continue on duplicate key errors
            try:
                collection.insert_many(cleaned_jobs, ordered=False)
                print("Jobs successfully stored in MongoDB.")
            except Exception as e:
                print(f"Some jobs were not inserted (likely duplicates): {e}")

        # Delete jobs older than 24 hours
        cutoff_time = datetime.now(UTC) - timedelta(hours=24)
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

@app.route('/metrics', methods=['GET'])
def get_metrics():
    try:
        job_count = collection.count_documents({})
        return jsonify({
            "total_jobs": job_count,
            "last_update": datetime.now(eastern_tz).strftime('%Y-%m-%d %H:%M:%S %Z')
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server on port 5000...")
    
    # Run scraper only if in the main process, not in the reloader
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        scrape_and_store_jobs()  
    
    app.run(port=5000, debug=True)