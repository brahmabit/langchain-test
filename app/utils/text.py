from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_document(content: str, chunk_size=2000, chunk_overlap=400):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(content)
