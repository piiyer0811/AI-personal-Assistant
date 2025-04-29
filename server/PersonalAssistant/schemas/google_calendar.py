get_calendar_events_function = {
    "name": "get_calendar_events",
    "description": "Fetches events from the user's Google Calendar between specified times.",
    "parameters": {
        "type": "object",
        "properties": {
            "user_email": {
                "type": "string",
                "description": "The user's email or calendar ID (usually 'primary')."
            },
            "access_token": {
                "type": "string",
                "description": "Google OAuth access token for accessing user's calendar."
            },
            "time_start": {
                "type": "string",
                "description": "Start time in ISO 8601 format (e.g., '2025-04-30T00:00:00Z')."
            },
            "time_end": {
                "type": "string",
                "description": "End time in ISO 8601 format (e.g., '2025-04-30T23:59:59Z')."
            },
            "keyword": {
                "type": "string",
                "description": "Optional keyword to filter events by summary (e.g., 'lecture')."
            },
            "max_results": {
                "type": "integer",
                "description": "Maximum number of events to return."
            },
            "time_zone": {
                "type": "string",
                "description": "Time zone for formatting response times."
            }
        },
        "required": ["user_email", "access_token", "time_start", "time_end"]
    }
}