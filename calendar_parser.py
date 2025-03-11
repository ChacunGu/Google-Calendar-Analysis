import os
import csv
import datetime
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the required scope
SCOPES = ['https://www.googleapis.com/auth/calendar.events.readonly']

def authenticate():
    creds = None
    token_path = "token.json"

    # Load existing credentials if available
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # If credentials are invalid, request new authentication
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
            creds = flow.run_local_server(port=0, open_browser=False)

        # Save credentials for future use
        with open(token_path, "w") as token_file:
            token_file.write(creds.to_json())

    return creds

def get_events_by_keyword(service, keyword):
    time_min = "2024-10-01T00:00:00Z" # From October 1st
    time_max = datetime.datetime.combine(datetime.datetime.now(), datetime.datetime.min.time()).strftime('%Y-%m-%dT%H:%M:%SZ') # To midnight today

    events_result = service.events().list(
        calendarId="primary",
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = events_result.get("items", [])

    # Filter events by keyword in the summary/title
    filtered_events = [
        {
            "start": event["start"].get("dateTime", event["start"].get("date")),
            "end": event["end"].get("dateTime", event["end"].get("date")),
            "title": event.get("summary", "No Title")
        }
        for event in events if keyword.lower() in event.get("summary", "").lower()
    ]

    return filtered_events

def save_to_csv(events, filename="events.csv"):
    """Save events to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Start Date", "End Date", "Event Title"])

        for event in events:
            writer.writerow([event["start"], event["end"], event["title"]])

    print(f"Events saved to {filename}")

if __name__ == "__main__":
    creds = authenticate()
    service = build("calendar", "v3", credentials=creds)

    keyword = input("Enter keyword to search for events: ")
    matching_events = get_events_by_keyword(service, keyword)

    if matching_events:
        save_to_csv(matching_events)
        for event in matching_events:
            print(f"{event['start']} - {event['end']}: {event['title']}")
    else:
        print("No matching events found.")
