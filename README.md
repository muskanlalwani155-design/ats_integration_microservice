# Serverless ATS Microservice (Zoho Recruit Integration)

This project integrates with **Zoho Recruit ATS** to provide a unified API for fetching jobs, creating candidates, and listing applications.

> ** NOTE FOR EVALUATOR:** To make testing easier for you, I have **pre-configured the API Credentials directly in the code.** You do not need to create an account or generate tokens manually. Just follow the **"How to run the service locally"** section below.

---

## 1. How to create free trial/sandbox in your ATS
We are using **Zoho Recruit** as our ATS. Here is how to set up a sandbox environment:

1. Visit the [Zoho Recruit Sign Up Page](https://www.zoho.com/recruit/).
2. Sign up for a free account.
3. Select the **"Corporate HR"** edition during setup.
4. Once logged in, you will have access to a 15-day free trial which acts as your Sandbox environment.
5. Create a dummy Job Opening (e.g., "Python Developer") to start testing.

my .env file tokens are these
ZOHO_CLIENT_ID=1000.75SM1MFKYRW1GKDUMAF5GK5FTI3OEX
ZOHO_CLIENT_SECRET=e70cddb75fcc920575285930f8b13c6ed9846893cc
ZOHO_REFRESH_TOKEN=1000.18acb5e976c07da14ff8f2511a9df094.183c1706e73c9c700daee728377b8bca
ATS_BASE_URL=https://recruit.zoho.in/recruit/v2

---

## 2. How to generate API key / token
Zoho Recruit uses **OAuth 2.0** for authentication. Follow these steps to generate the required tokens:

1. **Register Client:**
   - Go to [Zoho API Console](https://api-console.zoho.in/).
   - Click "Add Client" > "Server-based Applications".
   - Enter `http://localhost:3000/callback` as the Authorized Redirect URI.
   - Copy the **Client ID** and **Client Secret**.

2. **Generate Grant Token (One-time code):**
   - Paste this URL in your browser (replace `YOUR_CLIENT_ID`):
     `https://accounts.zoho.in/oauth/v2/auth?scope=ZohoRecruit.modules.ALL&client_id=YOUR_CLIENT_ID&response_type=code&access_type=offline&redirect_uri=http://localhost:3000/callback`
   - Click "Accept". Copy the `code` from the redirect URL.

3. **Generate Refresh Token:**
   - Make a POST request to `https://accounts.zoho.in/oauth/v2/token` with `client_id`, `client_secret`, `grant_type=authorization_code`, and the `code` from the previous step.
   - The response will contain the **Refresh Token**.

*(Note: These credentials have already been generated and embedded in the code for this submission.)*

---

## 3. How to run the service locally
Since the environment is pre-configured, follow these simple steps:

1. **Install Dependencies:**
   Open your terminal in the project folder and run:
   ```bash
   npm install
Start the Server: Run the following command to start the offline server:

Bash
serverless offline start
Verify: The service will start running at http://localhost:3000.

4. Example curl/Postman calls
You can use the links below to test the API immediately in your browser or Postman.

A. List All Jobs (GET)
Fetches all open job listings from the ATS. 👉 Link: http://localhost:3000/dev/jobs

cURL:

Bash
curl --location --request GET 'http://localhost:3000/dev/jobs'
B. Create Candidate (POST)
Creates a candidate and associates them with the "Python Backend Developer" job.

cURL:

Bash
curl --location --request POST 'http://localhost:3000/dev/candidates' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Evaluator Test",
    "email": "evaluator.test@example.com",
    "phone": "9999999999",
    "resume_url": "[https://linkedin.com/in/test](https://linkedin.com/in/test)",
    "job_id": "210479000000354814"
}'
C. View Applications (GET)
Lists all candidates applied to the specific Job ID (210479000000354814). 👉 Link: http://localhost:3000/dev/applications?job_id=210479000000354814

cURL:

Bash
curl --location --request GET 'http://localhost:3000/dev/applications?job_id=210479000000354814'
