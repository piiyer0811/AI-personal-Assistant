get_calendar_events_function = {
    "name": "get_calendar_events",
    "description": "Fetches events from the user's Google Calendar between specified times.",
    "parameters": {
        "type": "object",
        "properties": {
           
            "time_start": {
                "type": "string",
                "description": "Start time in ISO 8601 format (e.g., '2025-04-30T00:00:00Z')."
            },
            "time_end": {
                "type": "string",
                "description": "End time in ISO 8601 format (e.g., '2025-04-30T23:59:59Z')."
            }
        }
    }
}