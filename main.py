import requests
from datetime import datetime
import os

GENDER = "M"
AGE = 25
WEIGHT = 72.5
HEIGHT = 179.5

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]

nutrition_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["SHEET_ENDPOINT"]


exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "Content-Type": "application/json"
}

nutrition_parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT,
    "height_cm": HEIGHT,
    "age": AGE
}

response = requests.post(url=nutrition_endpoint, json=nutrition_parameters, headers=headers)
result = response.json()


today_date = datetime.now().strftime("%d/%m/%Y")
today_now = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": today_now,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }
    # Basic Authentication
    # sheet_response = requests.post(url=sheet_endpoint, json=sheet_inputs, auth=("Magomed", "maga112233"))

    # Bearer Token Authentication
    bearer_headers = {
        "Authorization": f"Bearer {os.environ['TOKEN']}"
    }
    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        headers=bearer_headers
    )
