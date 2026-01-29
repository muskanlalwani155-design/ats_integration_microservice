ATS Integration Microservice (Python & Serverless)
This microservice provides a unified REST API to interact with an Applicant Tracking System (ATS). It is built using Python and the Serverless Framework, designed to run on AWS Lambda.

1. How to create ATS Sandbox (Beeceptor)
Since this project integrates with a mock ATS, we use Beeceptor to simulate the ATS backend.

Go to Beeceptor.

Enter a unique endpoint name (e.g., muskan-ats-api) and click Create Endpoint.

Mock Rules Setup:

Create a GET /jobs rule to return a list of open positions.

Create a POST /candidates rule to accept candidate applications.

Create a GET /applications rule to list candidates for a specific job.

2. How to generate API Key / Token
For this integration, we use a static Authorization Token to secure the connection:

You can define any alphanumeric string as your secret token (e.g., my-secret-ats-token-2026).

This token must be added to your environment variables in the serverless.yml file under the key ATS_API_KEY.

In a production environment, this would be generated via the ATS settings dashboard.

3. How to run the service locally
To run and test the microservice on your machine:

Install Serverless Framework:

Bash
npm install -g serverless
Install Plugin for Local Testing:

Bash
npm install serverless-offline --save-dev
Set Environment Variables: Ensure your serverless.yml has the following:

YAML
environment:
  ATS_BASE_URL: https://your-endpoint.beeceptor.com
  ATS_API_KEY: your-static-token
Start the Service:

Bash
serverless offline
The service will start at http://localhost:3000/dev/.

4. Example API Calls
A. Get All Open Jobs
Method: GET

Endpoint: /jobs

Bash
curl http://localhost:3000/dev/jobs
B. Create a New Candidate
Method: POST

Endpoint: /candidates

PowerShell
Invoke-RestMethod -Uri "http://localhost:3000/dev/candidates" -Method Post -Body '{"name": "Rahul Sharma", "email": "rahul@example.com", "phone": "9988776655", "resume_url": "https://link.com/cv.pdf", "job_id": "102"}' -ContentType "application/json"
C. Get Applications for a Job
Method: GET

Endpoint: /applications?job_id=101

Bash
curl http://localhost:3000/dev/applications?job_id=101