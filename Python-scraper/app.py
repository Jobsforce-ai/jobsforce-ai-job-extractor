from flask import Flask, jsonify
from flask_cors import CORS
import math
from jobspy import scrape_jobs
from datetime import date, datetime
from pymongo import MongoClient
from models import insert_job 
app = Flask(__name__)
CORS(app)

try:
    client = MongoClient(MONGO_URI)
    db = client['job_database']  
    collection = db['jobs'] 

    print("Connected to MongoDB successfully!")
except Exception as e:
    print(f" MongoDB Connection Failed: {e}")

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
    return [job for job in jobs if job.get('description')]

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    try:
        print("Fetching jobs from jobspy...")  # Debugging statement

        jobs = scrape_jobs(
            site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"],
            search_term="Software Engineer",
            location="India",
            results_wanted=1000,
            hours_old=24,
            country_indeed="india"
        )

        # Check if jobs were fetched successfully
        if jobs.empty:
            print("No jobs fetched!")  # Debugging
            return jsonify({"error": "No jobs found"}), 404

        print(f"Total jobs fetched: {len(jobs)}")  # Debugging

        jobs_dict = jobs.to_dict(orient="records")
        jobs_serializable = [clean_data(job) for job in jobs_dict]
        jobs_with_description = filter_jobs_with_description(jobs_serializable)

        print(f"Jobs after filtering descriptions: {len(jobs_with_description)}")  # Debugging

        if jobs_with_description:
            for job in jobs_with_description:
                insert_job(job)
            print("Jobs successfully stored in MongoDB.")

        return jsonify(jobs_with_description)

    except Exception as e:
        print(f"Error occurred: {e}")  # Debugging
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting Flask server on port 5000...")  # Debugging
    app.run(port=5000, debug=True)
