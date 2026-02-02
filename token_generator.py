import requests

url = "https://accounts.zoho.in/oauth/v2/token"
data = {
    "code": "1000.2fb4bb981e5add324c6601068e5cefbc.79f6e84678d96b0f2610e00cf6e9a2f5",
    "client_id": "1000.3TV8BVFG960MXVVJWGP8QVND9KA4EY",
    "client_secret": "a3d7aa2c9f2281a1fc5e61a82cf15e38d95d50a1b5",
    "grant_type": "authorization_code",
    "redirect_uri": "https://api-console.zoho.in/"
}

response = requests.post(url, data=data)
print(response.json())