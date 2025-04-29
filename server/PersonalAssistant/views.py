from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

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

            if not all([access_token, id_token, user_prompt]):
                return JsonResponse({"error": "Missing required fields."}, status=400)

            # TODO: Use access_token to access Google APIs
            # TODO: Use id_token to verify the user's identity
            # TODO: Use user_prompt with Gemini API or something else

            return JsonResponse({
                "message": "Received successfully.",
                "access_token": access_token,
                "id_token": id_token,
                "user_prompt": user_prompt
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON."}, status=400)

    return JsonResponse({"error": "Only POST allowed."}, status=405)

