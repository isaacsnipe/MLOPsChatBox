import os
import os.path
import pickle

# Miscelleneous
import pinecone
from dotenv import dotenv_values
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain
from langchain.chat_models import ChatOpenAI
# Langchain imports
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.vectorstores import Pinecone
from pydantic import BaseSettings

# Prompts
from core.condense_prompt import CONDENSE_PROMPT
# Import custom decorators
from core.decorators import timer
# Import environment variables
from core.qa_prompt import QA_PROMPT

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

class ChatBot:
    def __init__(self):
        """
        Initialize the ChatBot object.
        This is called by __init__ and should not be called by user code
        """
        self.llm = None

    @timer
    def initialize(self):
        """
        Initialize OpenAI model. This is called before any queries are made.
        The model must be loaded with : func : ` load_qa_chain `
        """
        # Load the OpenAI chain and load the chain.
        if self.llm is None:
            self.embeddings = OpenAIEmbeddings(
                model="text-embedding-ada-002", openai_api_key=openai_api_key
            )
            
            self.llm = ChatOpenAI(
                model_name="gpt-3.5-turbo",
                temperature=temperature,
                openai_api_key=openai_api_key,
                streaming=True,
            )  # max temperature is 2 least is 0

            self.chain = load_qa_chain(self.llm, chain_type="stuff")

    def get_answer(self, query, conversation_id):
        """
        Returns a list of answers. This is used to get the most relevant answer for a query. It uses pinecone to search for similar documents and a retriever to retrieve the most relevant answer

        Args:
                query: The query to be matched

        Returns:
                A list of answer
        """
        chat_history_pickle = f"{document_folder}/{conversation_id}/history.pickle"

        try:
            with open(chat_history_pickle, "rb") as f:
                self.chat_history = pickle.load(f)
        except Exception:
            self.chat_history = []

        self.memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.query = query
        pinecone.init(api_key=pinecone_api_key,
                      environment=pinecone_api_region)

        self.vector_store = Pinecone.from_existing_index(
            index_name=pinecone_index_name,
            embedding=self.embeddings,
            text_key="text",
            namespace=conversation_id,
        )

        self.retriever = self.vector_store.as_retriever(
            search_kwargs={"k": number_of_sources},
            qa_template=QA_PROMPT,
            question_generator_template=CONDENSE_PROMPT,
        )  # 9 is the max sources

        model = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=temperature,
            openai_api_key=openai_api_key,
            streaming=True,
        )  # max temperature is 2 least is 0

        self.qa = ConversationalRetrievalChain.from_llm(
            llm=model, retriever=self.retriever, return_source_documents=True
        )

        self.result = self.qa(
            {"question": self.query, "chat_history": self.chat_history}
        )

        self.chat_history.append((self.query, self.result["answer"]))

        # Writing to a pickle file
        with open(chat_history_pickle, "wb") as f:
            pickle.dump(self.chat_history, f)

        source_documents = self.result["source_documents"]

        # Document details
        parsed_documents = []
        for doc in source_documents:
            parsed_doc = {
                "page_content": doc.page_content,
                "metadata": {
                    "page_number": doc.metadata.get("page", (doc.metadata.get("page_number", 1) - 1)),
                    "source": doc.metadata.get("source", ""),
                    "total_pages": doc.metadata.get("total_pages", 0),
                },
            }
            parsed_documents.append(parsed_doc)

        self.result["source"] = []
        self.result["page_number"] = []

        for doc in parsed_documents:
            self.result["source"].append(doc["metadata"]["source"])
            self.result["page_number"].append(doc["metadata"]["page_number"])

        self.response = {
            "prompt": query,
            "response": self.result["answer"],
            "page_number": list(set([
                f"Page {int(page_number) + 1} - {source.split('/')[-1]}"
                for source, page_number in zip(
                    self.result["source"], self.result["page_number"]
                )
            ])),
            "sources": self.result["source"] #source_documents 
        }

        return self.response


class Settings(BaseSettings):
    APP_NAME: str = "ChatBot"
    version: str = "1.0"
    releaseId: str = "1.1"
    API_V1_STR: str = "/api/v1"
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


settings = Settings()

chatbot = ChatBot()
