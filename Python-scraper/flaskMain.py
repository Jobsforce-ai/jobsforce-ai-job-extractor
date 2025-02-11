from flask import Flask, jsonify
from flask_cors import CORS
import json
import math
from jobspy import scrape_jobs
from datetime import date, datetime
import os

app = Flask(__name__)
CORS(app)

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

def filter_jobs_with_description(jobs):
    return [job for job in jobs if job.get('description')]

def convert_nan(obj):
    if isinstance(obj, list):
        return [convert_nan(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: convert_nan(v) for k, v in obj.items()}
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    return obj

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    try:
        jobs = scrape_jobs(
            site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
            search_term="Software Engineer",
            location="India",
            results_wanted=20,
            hours_old=72,
            country_indeed="india"
        )
        
        jobs_dict = jobs.to_dict(orient="records")
        jobs_serializable = [clean_data(job) for job in jobs_dict]
        jobs_with_description = filter_jobs_with_description(jobs_serializable)
        
        # Additional NaN cleaning
        cleaned_jobs = convert_nan(jobs_with_description)
        
        return jsonify(cleaned_jobs)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)