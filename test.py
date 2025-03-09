from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set up API credentials (replace 'path/to/your/credentials.json' with your actual path)
credentials = service_account.Credentials.from_service_account_file(r'C:\Users\priya\OneDrive\Desktop\majorprojectspeechrecognition-f3c5a9b70b51.json')
meet_service = build('meet', 'v1', credentials=credentials)

def create_meeting():
    # Create a new Google Meet link
    meeting = meet_service.conferences().create(
        body={"conferenceSolutionKey": {"type": "hangoutsMeet"}}
    ).execute()
    return meeting['conferenceData']['entryPoints'][0]['uri']

def get_meeting_details(meeting_id):
    # Retrieve details of a scheduled meeting
    meeting = meet_service.conferences().get(conferenceId=meeting_id).execute()
    return meeting

# Additional functions for managing meetings, access control, and integration with Google Calendar
# ...

# Example usage:
new_meeting_link = create_meeting()
print("New Meeting Link:", new_meeting_link)

# Assuming you have a meeting ID from a scheduled meeting
meeting_details = get_meeting_details('your_meeting_id')
print("Meeting Details:", meeting_details)
