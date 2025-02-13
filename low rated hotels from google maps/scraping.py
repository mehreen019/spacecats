from requests import get
import requests
import json
import os
import csv
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the API key and endpoint
API_KEY = os.getenv('MAPS_API_KEY')
URL = f"https://places.googleapis.com/v1/places:searchText?key={API_KEY}"

# Define the request payload
payload = {
    #"textQuery": "independent hotel OR motel OR inn OR bed and breakfast OR lodge OR resort OR guesthouse OR boutique hotel OR vacation rental -chain -marriott -hilton -holiday inn -best western -comfort inn -days inn -super 8",
    "textQuery": "independent lodge",
    "pageSize": 20,
    "locationRestriction": {
        "rectangle": {
            "low": {
                "latitude": 31.3322,
                "longitude": -114.8166
            },
            "high": {
                "latitude": 37.0043,
                "longitude": -109.0452
            }
        }
    }
}

# Define headers
headers = {
    "Content-Type": "application/json",
    "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.websiteUri,places.rating,places.nationalPhoneNumber,places.googleMapsLinks,nextPageToken"
}

# Make the POST request
response = requests.post(URL, headers=headers, json=payload)

if response.status_code != 200:
    print(f"Error details: {response.text}")

results = []  # List to store results

cnt=0

if response.status_code == 200:
    data = response.json()
    places = data.get("places", [])
    for place in places:
        # Consistent rating check with error handling
        rating = place.get("rating")
        if rating is None or rating <= 4.0:
            results.append(place)
    next_page_token = data.get("nextPageToken")
    print('next_page_token ',next_page_token)


    # Fetch additional pages (up to 100 requests or no nextPageToken)
    while next_page_token and len(results) < 1000:
        cnt+=1
        time.sleep(2)  # Delay to ensure nextPageToken is valid
        
        # Debug print
        print(f"Fetching page {cnt}, current results: {len(results)}")
        
        next_page_response = requests.post(URL, headers=headers, json={**payload, "pageToken": next_page_token})
        if next_page_response.status_code == 200:
            next_page_data = next_page_response.json()
            places = next_page_data.get("places", [])
            for place in places:
                if place.get("rating") is None or place.get("rating") <= 4.0:
                    results.append(place)
            next_page_token = next_page_data.get("nextPageToken")
            print('next_page_token ',next_page_token)

        else:
            print(f"Error fetching next page: {next_page_response.status_code}")
            break
else:
    print(f"Error with initial request: {response.status_code}")

# Write results to CSV
if results:
    with open("places_results.csv", "a", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["name", "formatted_address","websiteUri","rating", "nationalPhoneNumber", "googleMapsLinks"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for place in results:
            writer.writerow({
                "name": place.get("displayName", {}).get("text"),
                "formatted_address": place.get("formattedAddress"),
                "websiteUri": place.get("websiteUri"),
                "rating": place.get("rating"),
                "nationalPhoneNumber": place.get("nationalPhoneNumber"),
                "googleMapsLinks": place.get("googleMapsLinks", {}).get("placeUri"),
            })

    print(f"Successfully saved {len(results)} places to places_results.csv")
    print(f"Number of requests made: {cnt}")
else:
    print("No results found.")

