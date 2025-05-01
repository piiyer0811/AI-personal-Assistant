# ============================
# ✅ PHASE 1 - TODO CHECKLIST
# ============================

# ----------------------------
# 📁 PROJECT STRUCTURE SETUP
# ----------------------------

# [x] Set up virtual environment inside `server/`
# [x] Install required packages: django, python-dotenv, requests, etc.
# [x] Create Django project and app
# [x] Create .env file and add GEMINI_API_KEY
# [x] Create folders:
#     - decision_engine.py  # Gemini client + decision logic
#     - google_calendar.py  # Google Calendar API calls
#     - functions.py        # Gemini function call schemas
#     - views.py            # Expose summarise_user_prompt endpoint

# ----------------------------
# 🚀 MAIN FLOW (SUMMARY LOGIC)
# ----------------------------

# [ ] Frontend sends POST to Django API with:
#     - access_token
#     - id_token
#     - user_prompt

# [ ] Backend Django view receives request and extracts data

# [ ] Pass `user_prompt` to decision_engine.py
#     - [ ] Gemini decides whether a function call is needed
#     - [ ] If yes → extract function_name and args

# [ ] If function_name is get_events:
#     - [ ] Pass access_token + timeMin + timeMax to google_calendar.py
#     - [ ] Get list of user’s events

# [ ] Send user_prompt + raw event data back to Gemini
#     - [ ] Receive natural language response like:
#           "You have lectures at 2 PM and 6 PM on Tuesday."

# [ ] Return final response back to frontend

# ----------------------------
# 🛠️ EXTRA DEV TASKS
# ----------------------------

# [ ] Add CSRF exempt to Django API endpoint
# [ ] Secure .env + add to .gitignore
# [ ] Log Gemini and Calendar errors properly
# [ ] Unit tests for:
#     - decision_engine.py
#     - google_calendar.py
# [ ] Catch token expiration and show auth error
