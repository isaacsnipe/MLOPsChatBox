import os

from langchain.text_splitter import RecursiveCharacterTextSplitter


def get_new_data_path(directory):
    data_folders = os.listdir(directory)
    if data_folders == []:
        os.mkdir(os.path.join(directory, "data_0"))
        return os.path.join(directory, "data_0")
    else:
        idx_max = max([int(folder.split("_")[-1]) for folder in data_folders])
        # Check the last data folder
        idx_next = idx_max + 1
        # Create a new folder
        new_folder_path = os.path.join(directory, f"data_{idx_next}")
        if not os.path.exists(new_folder_path):
            os.mkdir(new_folder_path)
        return new_folder_path


# Define split_docs function
def split_docs(document_loader, chunk_size=1000, chunk_overlap=20):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    docs = text_splitter.split_documents(document_loader)
    return docs
