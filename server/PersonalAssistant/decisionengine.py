from google import genai
from google.genai import types
import os
from personalassistant.schemas import google_calendar
from personalassistant.functions import google_calendar as google_calendar_functions
from personalassistant import contextconverter
import json
from dotenv import load_dotenv



 # Send request with function declarations

def inject_context_args(function_name, function_args, user_context_meta):
    # List of functions that require context data
    functions_that_need_context = ["get_calendar_events"]

    if function_name in functions_that_need_context:
        function_args["user_email"] = user_context_meta["user_email"]
        function_args["access_token"] = user_context_meta["access_token"]
        function_args["time_zone"] = user_context_meta.get("time_zone")
    
    return function_args

 

def decide_and_summarise(access_token,id_token,context,user_prompt, email_id,time_zone):


    user_context_meta = {
        "user_email": email_id,
        "access_token": access_token,
        "time_zone": time_zone
    }

    load_dotenv()
    # Configure the client and tools
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    tools = types.Tool(function_declarations=[google_calendar.get_calendar_events_function])
    config = types.GenerateContentConfig(tools=[tools])

# Step 1: Append user prompt to context
    context.append({"role": "user", "content": user_prompt})

    context_object= { "conversation_history": context}

# Step 2: Call Gemini to decide what to do
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=contextconverter.context_to_contents(context_object),
        config=config,
    )


    reply = response.candidates[0].content

    # Step 3: If function call is suggested
    if reply.parts and reply.parts[0].function_call:
        function_call = reply.parts[0].function_call
        function_name = function_call.name
        function_args = function_call.args

        # Inject context information if needed
        function_args = inject_context_args(function_name, function_args, user_context_meta)


        print(f"Function to call: {function_name}")
        print(f"Arguments: {function_args}")

    # Step 4: Switch-case structure for function dispatch

        function_dispatch = {
            "get_calendar_events": lambda args: google_calendar_functions.get_calendar_events(**args),
            # Add other functions here if needed
            # "another_function": lambda args: another_function(args),
        }

        # Call the function based on function_name
        if function_name in function_dispatch:
            result = function_dispatch[function_name](function_args)
        else:
            return {"reply": f"Unknown function: {function_name}", "status": "error"}
        
    # Step 5: Add function call and function response to context    
        context.append({
            "role": "model",
            "content": {
                "function_call": {
                    "name": function_name,
                    "args": function_args
                },
                "text": f"Function {function_name} executed."
            }
        })

        context.append({
            "role": "model",
            "content": json.dumps(result)  # Function output as JSON string
        })

        context_object= { "conversation_history": context}


    # Step 6: Ask Gemini to summarise function result
        summary_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contextconverter.context_to_contents(context_object),
            config=config,
        )

        return {
            "reply": summary_response.text,
            "status": "success"
        }

    # Step 7: If no function is needed, just return Gemini's natural response
    else:
        context.append({"role": "model", "content": response.text})
        return {
            "reply": response.text , 
            "status": "success"
        }