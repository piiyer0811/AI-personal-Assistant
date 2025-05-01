from .firebase_config import db
from datetime import datetime, timezone

def get_user_context(id_token):
    """
    Fetches user context from Firebase Firestore by id_token.

    Args:
        id_token (str): Unique identifier for the user.

    Returns:
        dict or None: The user context document if it exists, else None.
    """
    doc_ref = db.collection("users").document(id_token)
    doc = doc_ref.get()

    if doc.exists:
        return doc.to_dict()
    else:
        return None

def create_user_context(id_token: str):
    """
    Creates a new Firestore document for the user using greeting and preprompt from system_messages.
    """

    try:
        greeting_doc = db.collection("system_messages").document("greeting").get()
        preprompt_doc = db.collection("system_messages").document("preprompt").get()

        if not greeting_doc.exists or not preprompt_doc.exists:
            return {"status": "error", "message": "Greeting or Preprompt not found in Firebase."}

        greeting_text = greeting_doc.to_dict().get("text", "Hello! How can I assist you today?")
        preprompt_text = preprompt_doc.to_dict().get("text", "You are a helpful assistant.")

        context = [
            {"role": "system", "content": preprompt_text},
            {"role": "assistant", "content": greeting_text}
        ]

        db.collection("users").document(id_token).set({
            "conversation_history": context,
        })

        return {"context": context, "status": "success", "message": "User context created successfully."}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

def update_user_context(id_token, context):
    """
    Updates the conversation context for a user in Firebase.

    Args:
        id_token (str): User's ID token (used as document ID).
        new_context (list): Updated conversation history (list of message objects).
    """
    try:
        doc_ref = db.collection("users").document(id_token)
        doc_ref.update({"conversation_history": context})
        print("User context updated successfully.")
        return {"status": "success", "message": "User context updated successfully."}
    except Exception as e:
        print(f"Failed to update user context: {e}")
        return {"status": "error", "message": str(e)}
