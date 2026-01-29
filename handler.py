import json
import requests
import os


BASE_URL = os.environ.get('ATS_BASE_URL')
API_KEY = os.environ.get('ATS_API_KEY')

def get_jobs(event, context):
    try:
        response = requests.get(f"{BASE_URL}/jobs")
        ats_jobs = response.json()
        
        
        formatted_jobs = []
        for job in ats_jobs:
            if job.get("status") == "OPEN":
                formatted_jobs.append({
                    "id": str(job.get("id")),
                    "title": job.get("title"),
                    "location": job.get("location"),
                    "status": job.get("status"),
                    "external_url": job.get("external_url")
                })
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(formatted_jobs)
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

def create_candidate(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        
        
        response = requests.post(f"{BASE_URL}/candidates", json=body)

        return {
            "statusCode": 201,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Candidate created successfully", 
                "ats_response": response.json() if response.text else "Success"
            })
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

def get_applications(event, context):
    try:
        
        params = event.get('queryStringParameters') or {}
        job_id = params.get('job_id')

        
        
        url = f"{BASE_URL}/applications"
        if job_id:
            url += f"?job_id={job_id}"
            
        response = requests.get(url)
        apps = response.json()
        
        
        standardized_apps = []
        for app in apps:
            standardized_apps.append({
                "id": str(app.get('id', app.get('application_id', ''))),
                "candidate_name": app.get('candidate_name'),
                "email": app.get('email'),
                "status": app.get('status', 'APPLIED')
            })

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(standardized_apps)
        }
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}