import os
from datetime import datetime

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

from core.database import db
from core.oauth2 import get_current_user
from schemas.conversation import Conversation
from schemas.user import User

from dotenv import load_dotenv
load_dotenv()

# Get the value of the PINECONE_API_KEY environment variable
pinecone_api_key = os.environ.get("PINECONE_API_KEY")

# Get the value of the PINECONE_API_REGION environment variable
pinecone_api_region = os.environ.get("PINECONE_API_REGION")

# Get the value of the PINECONE_INDEX environment variable
pinecone_index_name = os.environ.get("PINECONE_INDEX_NAME")

# Get the value for the OPEN AI API key
openai_api_key = os.environ.get("OPEN_AI_API_KEY")

# Get the number of sources for the chatbot answer
number_of_sources = int(os.environ.get("NUMBER_OF_SOURCES", 2))

# Get the temperature parameter
temperature = int(os.environ.get("TEMPERATURE", 1))

# Get the path for the document folder
document_folder = os.environ.get("DOCUMENT_PATH")


router = APIRouter()


@router.get("/user", status_code=200)
async def get_conversations_by_user_id(current_user: User = Depends(get_current_user)):
    arr = (
        await db.conversation.find({"user_id": current_user.id})
        .sort("created_at", -1)
        .to_list(1000)
    )
    conversations = []
    for conversation in arr:
        conversations.append(Conversation(**conversation))
    return conversations


# Return a conversation using its id
@router.get("/{id}", status_code=200)
async def get_conversation_by_id(id, current_user: User = Depends(get_current_user)):
    conversation = await db.conversation.find_one({"_id": id})
    return Conversation(**conversation)


@router.post("/", status_code=200)
async def create_conversation(current_user: User = Depends(get_current_user)):
    new_conversation = jsonable_encoder(
        Conversation(
            user_id=current_user.id,
            title=datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
            started_at=datetime.now(),
            ended_at=datetime.now(),
        )
    )
    await db.conversation.insert_one(new_conversation)
    new_conversation_path = os.path.join(document_folder, new_conversation["_id"])
    os.makedirs(new_conversation_path, exist_ok=True)
    return new_conversation


@router.put("/{id}", status_code=200)
async def update_conversation_title(id, new_title: str, current_user: User = Depends(get_current_user)):
    # Check if the conversation exists
    conversation = await db.conversation.find_one({'_id': id})
    # Update the conversation title
    db.conversation.update_one(
        {'_id': id},
        {'$set': {'title': new_title}}
    )

    updated_conversation = await db.conversation.find_one({'_id': id})
    return updated_conversation


@router.delete("/{id}", status_code=200)
async def delete_conversation(id, current_user: User = Depends(get_current_user)):
    deleted_result = await db.conversation.delete_one({"_id": id})

    if deleted_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=[])

    raise HTTPException(status_code=404, detail=f"Conversation{id} not found")
