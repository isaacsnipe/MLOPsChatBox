import os
import pickle
import tempfile
from datetime import datetime
from typing import Dict, List

import pinecone
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.encoders import jsonable_encoder
from langchain.document_loaders import DirectoryLoader, PyMuPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone

from core.config import chatbot
from core.database import db
from core.oauth2 import get_current_user
from core.upload_utils import get_new_data_path, split_docs
from core.vector_store import VectorStore
from schemas import error, upload
from schemas.document import Document
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


@router.post(
    "/upload",
    response_model=upload.UploadOut,
    responses={
        400: {"model": error.InvalidDocumentError},
        500: {"model": error.MLModelNotFoundError},
    },
)
# TODO: Refactor code for uploading of files
async def upload_files(
    files: List[UploadFile],
    conversation_id: str,
    current_user: User = Depends(get_current_user),
):
    """
    Use this API endpoint to upload files for the context-aware QnA chatbot
    How to use:
    1. Upload your file(s)
    2. Click execute.
    3. JSON output will be generated with a response
    """
    response = {"info": None}

    print("Initializing data directory...")

  
    # Create the folder with the conversation_id if conversation_id exists
    conversation = await db.conversation.find_one({"_id": conversation_id})
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    elif jsonable_encoder(conversation)["user_id"] != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")
    else:
        conv_document_path = os.path.join(
            document_folder, jsonable_encoder(conversation)["_id"]
        )

    for uploaded_file in files:
        file_name = uploaded_file.filename
        file_content = uploaded_file.read()
        with open(os.path.join(conv_document_path, file_name), "wb") as file:
            file.write(uploaded_file.file.read())

            # Write document to db
            new_document = Document(
                conversation_id=conversation_id,
                title=file_name,
                uploaded_at=datetime.now(),
            )

            new_document = jsonable_encoder(new_document)
            inserted_document = await db.documents.insert_one(new_document)

        loader = DirectoryLoader(
            conv_document_path, glob="**/*.pdf", loader_cls=PyMuPDFLoader
        )
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=100
        )
        documents = text_splitter.split_documents(documents)

        pinecone.init(api_key=pinecone_api_key,
                      environment=pinecone_api_region)

        embeddings = OpenAIEmbeddings(
            model="text-embedding-ada-002", openai_api_key=openai_api_key
        )
        Pinecone.from_documents(
            documents,
            embeddings,
            index_name=pinecone_index_name,
            namespace=conversation_id,
        )

    response["info"] = f"{len(documents)} document chunks have been uploaded"

    return response
