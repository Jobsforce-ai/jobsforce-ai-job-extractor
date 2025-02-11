import json
import math
from jobspy import scrape_jobs
from datetime import date, datetime
import os
output_directory = "../backend"
os.makedirs(output_directory, exist_ok=True)
# Scrape job data
jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"],
    search_term="Software Engineer",
    location="India",
    results_wanted=50,
    hours_old=20,
    country_indeed="india"
)

# Convert DataFrame to a dictionary
jobs_dict = jobs.to_dict(orient="records")

# Function to convert non-serializable objects and replace NaN with None
def clean_data(obj):
    if isinstance(obj, (date, datetime)):  # Convert date and datetime objects
        return obj.isoformat()
    elif isinstance(obj, float) and math.isnan(obj):  # Replace NaN with None
        return None
    elif isinstance(obj, list):  # Recursively clean lists
        return [clean_data(item) for item in obj]
    elif isinstance(obj, dict):  # Recursively clean dictionaries
        return {key: clean_data(value) for key, value in obj.items()}
    return obj  


def filter_jobs_with_description(jobs):
    return [job for job in jobs if job.get('description')]


jobs_serializable = [clean_data(job) for job in jobs_dict]


jobs_with_description = filter_jobs_with_description(jobs_serializable)


with open("jobs_filtered.json", "w", encoding="utf-8") as f:
    json.dump(jobs_with_description, f, ensure_ascii=False, indent=4)



def replace_nan_with_null(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    def convert_nan(obj):
        if isinstance(obj, list):
            return [convert_nan(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: convert_nan(v) for k, v in obj.items()}
        elif isinstance(obj, float) and math.isnan(obj):
            return None
        else:
            return obj
    
    converted_data = convert_nan(data)
    
    with open(output_file, 'w') as f:
        json.dump(converted_data, f, indent=4)
    
    print(f"Converted {input_file} and saved to {output_file}")

input_file = "jobs_filtered.json"
output_file = os.path.join(output_directory, "jobs.json")
replace_nan_with_null(input_file, output_file)


print("Job data saved successfully in jobs_filtered.json")
