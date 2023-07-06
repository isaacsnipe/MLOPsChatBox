# Langchain imports
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Import custom decorators
from core.decorators import timer


class DataDirectory:
    def __init__(self, directory_path):
        """
        Initialize the DataDirectory class.
        This is called by __init__ and should not be called directly.
        The directory_path is used to find the files that need to be added to the directory list.

        Args:
                directory_path: The path to the directory where the data is
        """
        self.directory_path = directory_path

    @timer
    def split_docs(self, chunk_size=1000, chunk_overlap=20):
        """
        Splits documents into sub - documents. This is a method to use when you want to split a document into sub - documents.

        Args:
                chunk_size: The size of each chunk in the document. Default 1000. Larger chunks are more likely to take longer than the chunk size.
                chunk_overlap: The overlap between chunks. Default 20. Higher overlap is more likely to take longer than the chunk size.

        Returns:
                A list of Langchain "Document" objects that are part of the document.
        """
        loader = DirectoryLoader(self.directory_path)
        self.documents = loader.load()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )
        self.docs = self.text_splitter.split_documents(self.documents)
        self.len_tokens = len(self.docs)

        return self.docs
