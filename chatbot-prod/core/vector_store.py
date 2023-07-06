import pinecone
from langchain.vectorstores import Pinecone

# Import custom decorators
from core.decorators import timer
# Import environment variables
from core.env_var import *

# Get the value of the PINECONE_API_KEY environment variable
pinecone_api_key = (
    "d29e9203-c999-4e75-9a52-ff62b319c82c"  # os.environ.get("PINECONE_API_KEY")
)

# Get the value of the PINECONE_API_REGION environment variable
pinecone_api_region = (
    "asia-southeast1-gcp-free"  # os.environ.get("PINECONE_API_REGION")
)

# Get the value of the PINECONE_INDEX environment variable
pinecone_index_name = "chat-bot-1"  # os.environ.get("PINECONE_INDEX_NAME")


class VectorStore:
    def __init__(self):
        """
        Initialize the object. This is called by __init__ and should not be called directly by user code
        """
        pass

    def __repr__(self):
        """
        Returns a string representation of the VectorStore. This is useful for debugging purposes. The string representation will be the same as the string representation of the VectorStore but with a newline at the end.


        Returns:
                A string representation of the VectorStore ( " VectorStore " ) in the format : " VectorStore
        """
        return f"{VectorStore()}"

    @timer
    def initialize(
        self,
        docs,
        embeddings,
        index_name=pinecone_index_name,
        api_key=pinecone_api_key,
        environment=pinecone_api_region,
    ):
        """
        The environment to use. Defaults to'us - central '. If you don't specify this it will default to'us - central '

        Args:
                docs: A list of Pinyin documents to index.
                embeddings: A list of embeddings for each document
                index_name: The name of the index to use
                api_key: The API key to use
                environment
        """
        self.api_key = api_key
        self.environment = environment
        self.docs = docs
        self.embeddings = embeddings
        self.index_name = index_name
        pinecone.init(api_key=self.api_key, environment=self.environment)
        self.index = Pinecone.from_documents(
            self.docs,
            self.embeddings,
            index_name=self.index_name,
            namespace=pinecone_namespace,
        )
        return self

    def get_similar_docs(self, query, k=2, score=False):
        """
        Get similar documents from the index for a particular query.

        Args:
                query: The query to search for
                k: The number of similar documents to return
                score: If True the score will be returned instead of the score

        Returns:
                A list of Document objects that match the query. Note that the documents are sorted by similarity
        """
        # Returns a list of similar docs for the query.
        if score:
            similar_docs = self.index.similarity_search_with_score(query, k=k)
        else:
            similar_docs = self.index.similarity_search(query, k=k)
        return similar_docs


# Create a vector store object
vectore_store = VectorStore()
