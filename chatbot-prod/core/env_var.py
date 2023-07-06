import os

# Define the pinecone namespace
pinecone_namespace = "testing-pdf-2389203901"

# Get the value of the PINECONE_API_KEY environment variable
pinecone_api_key = os.environ.get("PINECONE_API_KEY")

# Get the value of the PINECONE_API_REGION environment variable
pinecone_api_region = os.environ.get("PINECONE_API_REGION")

# Get the value of the PINECONE_INDEX environment variable
pinecone_index_name = os.environ.get("PINECONE_INDEX_NAME")

# Get the value for the OPEN AI API key
openai_api_key = os.environ.get("OPEN_AI_API_KEY")

# Get the number of sources for the chatbot answer
number_of_sources = 2

# Get the temperature parameter
temperature = os.environ.get("TEMPERATURE")

# Get the path for the document folder
document_folder = os.environ.get("DOCUMENT_PATH")

