import requests
from datetime import datetime

def get_calendar_events(user_email, access_token, time_start, time_end, keyword=None, max_results=10, time_zone='UTC'):
    """
    Fetches calendar events between time_start and time_end using Google Calendar API.
    Filters by keyword if provided.
    """

    url = f"https://www.googleapis.com/calendar/v3/calendars/{user_email}/events"
    
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "timeMin": time_start,
        "timeMax": time_end,
        "singleEvents": True,
        "orderBy": "startTime",
        "maxResults": max_results,
        "timeZone": time_zone
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        events = data.get("items", [])
        if keyword:
            # Filter events by keyword in summary
            events = [event for event in events if keyword.lower() in event.get("summary", "").lower()]

        return {
            "success": True,
            "event_count": len(events),
            "events": [
                {
                    "summary": e.get("summary", "No Title"),
                    "start": e.get("start", {}).get("dateTime", e.get("start", {}).get("date")),
                    "end": e.get("end", {}).get("dateTime", e.get("end", {}).get("date")),
                }
                for e in events
            ]
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": str(e)
        }