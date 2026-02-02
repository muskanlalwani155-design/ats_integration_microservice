import json
import requests
import os

# 1. Token Helper (Timeout 30s for safety)
def get_access_token():
    url = "https://accounts.zoho.in/oauth/v2/token"
    data = {
        "refresh_token": os.environ.get('ZOHO_REFRESH_TOKEN'),
        "client_id": os.environ.get('ZOHO_CLIENT_ID'),
        "client_secret": os.environ.get('ZOHO_CLIENT_SECRET'),
        "grant_type": "refresh_token"
    }
    try:
        response = requests.post(url, data=data, timeout=30)
        return response.json().get("access_token")
    except:
        return None

# 2. GET /jobs (Standard JSON)
def get_jobs(event, context):
    try:
        token = get_access_token()
        headers = {"Authorization": f"Zoho-oauthtoken {token}"}
        base_url = os.environ.get('ATS_BASE_URL', '').rstrip('/')
        
        res = requests.get(f"{base_url}/Job_Openings", headers=headers, timeout=30)
        zoho_jobs = res.json().get("data", [])
        
        standard_jobs = []
        for job in zoho_jobs:
            standard_jobs.append({
                "id": job.get("id"),
                "title": job.get("Job_Opening_Name") or job.get("Posting_Title"),
                "location": job.get("City", "Remote"),
                "status": "OPEN" if job.get("Job_Opening_Status") == "In-progress" else "CLOSED",
                "external_url": f"https://recruit.zoho.in/recruit/Portal.na?jobid={job.get('id')}"
            })
        return {"statusCode": 200, "body": json.dumps(standard_jobs)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

# 3. POST /candidates (Create + Link)
def create_candidate(event, context):
    try:
        body = json.loads(event.get("body", "{}"))
        job_id = body.get("job_id")
        token = get_access_token()
        headers = {"Authorization": f"Zoho-oauthtoken {token}"}
        base_url = os.environ.get('ATS_BASE_URL', '').rstrip('/')

        # Step 1: Create
        cand_payload = {"data": [{"First_Name": body.get("name"), "Last_Name": "Candidate", "Email": body.get("email"), "Phone": body.get("phone"), "Website": body.get("resume_url")}]}
        cand_res = requests.post(f"{base_url}/Candidates", headers=headers, json=cand_payload, timeout=30)
        cand_info = cand_res.json()

        # Step 2: Associate
        if "data" in cand_info and job_id:
            cand_id = cand_info['data'][0]['details']['id']
            assoc_url = f"{base_url}/Job_Openings/{job_id}/Associate"
            
            requests.post(assoc_url, headers=headers, json={"data": [{"ids": [cand_id], "comments": "API Link"}]}, timeout=30)
            return {"statusCode": 201, "body": json.dumps({"message": "Success", "id": cand_id})}

        return {"statusCode": 400, "body": json.dumps(cand_info)}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}


def get_applications(event, context):
    try:
        params = event.get("queryStringParameters") or {}
        target_job_id = params.get("job_id")
        
        if not target_job_id:
            return {"statusCode": 400, "body": json.dumps({"error": "job_id missing"})}

        token = get_access_token()
        headers = {"Authorization": f"Zoho-oauthtoken {token}"}
        base_url = os.environ.get('ATS_BASE_URL', '').rstrip('/')
        
        
        url = f"{base_url}/Applications"
        res = requests.get(url, headers=headers, timeout=30)
        
        all_apps = res.json().get("data", [])
        standard_apps = []
        
        for app in all_apps:
            
            id_match = False
            
            
            if str(app.get("$Job_Opening_Id")) == str(target_job_id):
                id_match = True
            
            
            elif str(app.get("Job_Opening_ID")) == str(target_job_id):
                id_match = True
                
            if id_match:
                
                full_name = f"{app.get('First_Name', '')} {app.get('Last_Name', '')}".strip()
                
                standard_apps.append({
                    "id": app.get("id"),
                    "candidate_name": full_name or "Unknown", #
                    "email": app.get("Email") or app.get("Candidate_Email"), 
                    "status": app.get("Application_Status") or "APPLIED"
                })
        
        return {"statusCode": 200, "body": json.dumps(standard_apps)}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}