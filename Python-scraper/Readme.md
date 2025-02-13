
# Job Scraper API

This project consists of a Python script that scrapes job listings from multiple platforms (Indeed, LinkedIn, ZipRecruiter, Glassdoor, Google) and serves the data via a Flask API. A Node.js function fetches this data and provides it to clients.

## Features
- Scrapes job listings from multiple platforms (Indeed, LinkedIn, ZipRecruiter, Glassdoor, Google)
- Cleans and filters job data
- Provides an API endpoint using Flask
- Fetches job data in a Node.js backend

## Setup Instructions

### 1. Clone the Repository
```sh
git clone <repository-url>
cd <project-folder>
```

### 2. Set Up Python Virtual Environment
```sh
python -m venv venv
```
Activate the virtual environment:
- **Windows (Command Prompt):** `venv\Scripts\activate`
- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **Mac/Linux:** `source venv/bin/activate`

### 3. Install Python Dependencies
```sh
pip install -r requirements.txt
pip install -U python-jobspy
```

### 4. Run the Flask Server
```sh
python app.py
```
The server will start at `http://127.0.0.1:5000`

### 5. Set Up Node.js Backend 
npm i
```


### 7. Run Node.js Server
Run your Node.js application with:
```sh
node server.js
```

## API Endpoints

### **Flask API**
- **GET** `/api/jobs` - Returns job listings in JSON format.

### **Node.js API**
- **GET** `/api/getJobs` - Calls the Flask API and returns job listings.


