from google import genai
from google.genai import types
import os
from personalassistant.schemas import google_calendar
from personalassistant.functions import google_calendar as google_calendar_functions
import json
from dotenv import load_dotenv



 # Send request with function declarations

 

def decide_and_summarise(access_token,id_token,context,user_prompt):


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
        contents=context_object,
        config=config,
    )


    reply = response.candidates[0].content

    # Step 3: If function call is suggested
    if reply.parts and reply.parts[0].function_call:
        function_call = reply.parts[0].function_call
        function_name = function_call.name
        function_args = function_call.args

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
            "role": "system",
            "content": {
                "function_call": {
                    "name": function_name,
                    "args": function_args
                },
                "text": f"Function {function_name} executed."
            }
        })

        context.append({
            "role": "system",
            "content": json.dumps(result)  # Function output as JSON string
        })

        context_object= { "conversation_history": context}


    # Step 6: Ask Gemini to summarise function result
        summary_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=context_object,
            config=config,
        )

        return {
            "reply": summary_response.text,
            "status": "success"
        }

    # Step 7: If no function is needed, just return Gemini's natural response
    else:
        context.append({"role": "model", "content": reply.text})
        return {
            "reply": reply.text , 
            "status": "success"
        }