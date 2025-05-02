from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from personalassistant import firebase_helper
from personalassistant import decisionengine

# Create your views here.

from django.http import HttpResponse

@csrf_exempt  #authentication already handled here
def summarise_user_prompt(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)

            access_token = body.get("access_token")
            id_token = body.get("id_token")
            user_prompt = body.get("user_prompt")
            email_id= body.get("email_id")
            time_zone=body.get("time_zone")

            if not all([access_token, id_token, user_prompt, email_id,time_zone]):
                return JsonResponse({"message": "Missing required fields."}, status=400)
            
            context_history_result= firebase_helper.get_user_context(id_token)

            context= []

            if context_history_result:
                context= context_history_result.get("conversation_history")
            else:
                # TODO: Create User context
                context_creation_result= firebase_helper.create_user_context(id_token)
                if context_creation_result.get("status") != "success":
                    return JsonResponse({"message": context_creation_result.get("message")}, status=400)

                context= context_creation_result.get("context")
            # TODO: Use user_prompt with Gemini API or something else

            assistant_reply= decisionengine.decide_and_summarise(access_token,id_token,context,user_prompt,email_id,time_zone)

            context_updation_result = firebase_helper.update_user_context(id_token, context)

            if context_updation_result.get("status") == "error":
                return JsonResponse({"message": context_updation_result.get("message")}, status=400)

            if not assistant_reply:
                return JsonResponse({"message": "Unknown Error"}, status=400)
            
            if assistant_reply.get("status") == "error":
                return JsonResponse({"message": assistant_reply.get("message")}, status=400)
            
            # TODO: Use access_token to access Google APIs
            return JsonResponse({
                "message": "Received successfully.",
               "reply": assistant_reply.get("reply")
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON."}, status=400)

    return JsonResponse({"message": "Only POST allowed."}, status=405)

