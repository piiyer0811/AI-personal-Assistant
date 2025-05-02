from google.generativeai import types


def context_to_contents(context_object):
    formatted = []

    for item in context_object.get("conversation_history"):
        role = item.get("role")
        content = item.get("content")

        if isinstance(content, dict) and "function_call" in content:
            # Handle function call format
            formatted.append({
                "role": role,
                "parts": [
                    {
                        "function_call": content["function_call"]
                    }
                ]
            })
        else:
            # Handle regular text message
            formatted.append({
                "role": role,
                "parts": [
                    {
                        "text": content
                    }
                ]
            })

    return formatted