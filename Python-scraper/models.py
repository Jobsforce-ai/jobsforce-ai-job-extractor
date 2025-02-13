from pymongo import MongoClient
from datetime import datetime
from bson import ObjectId
from dotenv import load_dotenv
load_dotenv()
import os

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["job_database"]
collection = db["jobs"]

# Define a job schema as a dictionary
job_schema = {
    "id": str,  # Unique job identifier
    "site": str,  # Source of the job listing
    "job_url": str,  # Job URL
    "job_url_direct": str,  # Direct job URL (optional)
    "title": str,  # Job title
    "company": str,  # Company name
    "location": str,  # Job location
    "date_posted": datetime,  # Date job was posted
    "job_type": str,  # Job type (full-time, part-time, etc.)
    "salary": {
        "source": str,
        "interval": str,
        "min_amount": float,
        "max_amount": float,
        "currency": str
    },
    "is_remote": bool,
    "job_level": str,
    "job_function": str,
    "listing_type": str,
    "emails": list,
    "description": str,
    "company_details": {
        "industry": str,
        "url": str,
        "logo": str,
        "num_employees": int,
        "revenue": int,
        "description": str,
        "addresses": list
    },
    "created_at": datetime,
    "updated_at": datetime
}

# Function to validate and insert job data
def insert_job(job_data):
    job_data["created_at"] = datetime.utcnow()
    job_data["updated_at"] = datetime.utcnow()

    # Ensure data matches schema
    validated_job = {key: job_data.get(key, None) for key in job_schema}
    collection.insert_one(validated_job)
    print("Job inserted successfully!")

