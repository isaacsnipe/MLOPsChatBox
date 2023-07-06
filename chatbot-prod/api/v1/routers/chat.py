from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from core.config import chatbot
from core.database import db
from core.generate_title import gen_title
from core.oauth2 import get_current_user
from schemas import chat, error, message
from schemas.message import Message
from schemas.user import User

router = APIRouter()


@router.get(
    "/chat/{conversation_id}",
    responses={
        400: {"model": error.InvalidDocumentError},
        500: {"model": error.MLModelNotFoundError},
    },
)
async def get_messages(
    conversation_id: str, current_user: User = Depends(get_current_user)
):
    conversation = await db.conversation.find_one({"_id": conversation_id})
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    elif jsonable_encoder(conversation)["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    else:
        arr = (
            await db.messages.find({"conversation_id": conversation_id})
            .sort("sent_at", -1)
            .to_list(1000)
        )
        messages = []
        for message in arr:
            messages.append(Message(**message))
        return messages


@router.post(
    "/chat",
    response_model=chat.ChatOut,
    responses={
        400: {"model": error.InvalidDocumentError},
        500: {"model": error.MLModelNotFoundError},
    },
)
async def send_chat(
    message: str, conversation_id: str, current_user: User = Depends(get_current_user)
):
    """
    Use this API endpoint to access our context-aware chatbot.
    How to use:
    1. Enter a question you want to ask from your database
    2. Click execute.
    3. JSON output will ge be generated with a response
    """

    # TODO: Create a message entity in the database from the user

    # Ensure conversation exists and conversation belongs to current user
    conversation = await db.conversation.find_one({"_id": conversation_id})
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    elif jsonable_encoder(conversation)["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    else:
        answer = chatbot.get_answer(message, conversation_id)

        ai_message = Message(
            conversation_id=conversation_id,
            prompt=answer["prompt"],
            response=answer["response"],
            sources=",".join(map(str, answer["sources"])),
            page_number=",".join(map(str, answer["page_number"])),
            sent_at=datetime.now(),
        )
        ai_message = jsonable_encoder(ai_message)

        db.messages.insert_one(ai_message)

        # Edit title and ended_at fields for conversation
        chat_title = gen_title(answer["response"])

        conversation_update = {"title": chat_title, "ended_at": datetime.now()}
        await db["conversation"].update_one(
            {"_id": conversation_id}, {"$set": conversation_update}
        )

    return answer
