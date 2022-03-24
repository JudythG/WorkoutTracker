import requests
from datetime import datetime
from requests.auth import HTTPBasicAuth
import os

SHEETY_USERNAME = os.environ.get("SHEETY_USERNAME")
SHEETY_PASSWORD = os.environ.get("SHEETY_PASSWORD")
WORKOUT_TRACKER_URL = os.environ.get("WORKOUT_TRACKER_URL")
NUTRITIONIX_API_KEY = os.environ.get("NUTRITIONIX_API_KEY")
NUTRITIONIX_ID = os.environ.get("NUTRITIONIX_ID")
NUTRITIONIX_BASE_URL = "https://trackapi.nutritionix.com/"
EXERCISE_ENDPOINT = NUTRITIONIX_BASE_URL + "/v2/natural/exercise"
EXERCISE_HEADER = {
    "x-app-id": NUTRITIONIX_ID,
    "x-app-key": NUTRITIONIX_API_KEY,
    "x-remote-user-id": "0",
}

exercise_body = {
    "query": "walked 30 minutes and meditated for 15 minutes",
}

response = requests.post(url=EXERCISE_ENDPOINT, headers=EXERCISE_HEADER, json=exercise_body)
response.raise_for_status()
today = datetime.now()

for exercise in response.json()['exercises']:
    sheety_payload = {
        "workout": {
            "date": today.strftime("%d/%m/%Y"),
            "time": today.strftime("%H:%M:%S"),
            "exercise": exercise['user_input'],
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories'],
        }
    }

    response = requests.post(url=WORKOUT_TRACKER_URL, json=sheety_payload, auth=HTTPBasicAuth(SHEETY_USERNAME, SHEETY_PASSWORD))
    response.raise_for_status()
    print(response.status_code)


