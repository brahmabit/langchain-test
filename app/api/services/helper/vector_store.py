from langchain_core.vectorstores import InMemoryVectorStore
from langchain.vectorstores import FAISS
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain.embeddings.openai import OpenAIEmbeddings
import faiss

import asyncio


class VectorStoreSingleton():
    _instance = None 

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(VectorStoreSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"): 
            self.embeddings = OpenAIEmbeddings()
            #self.vector_store = InMemoryVectorStore(embedding=self.embeddings)
            index = faiss.IndexFlatL2(1536)  
            self.vector_store = FAISS(embedding_function=self.embeddings, index=index, docstore=InMemoryDocstore(), index_to_docstore_id={})
            self._initialized = True
            self._last_used_id = 0

    def add_documents(self, document, metadata: dict):
        document.metadata = metadata
        self.vector_store.add_documents([document])

    def add_document_chunks(self, chunks, metadata):
        for chunk in chunks:
            self.vector_store.add_texts([chunk], [metadata])

    async def embed_chunks_in_batches(self, chunks: list[str], metadata: dict, batch_size: int = 10):
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]  # Get a batch of chunks
            embeddings = await asyncio.to_thread(self.embeddings.embed_documents, batch)
    
            self._instance.vector_store.add_embeddings(text_embeddings=zip(batch, embeddings), metadatas=[metadata] * len(batch))

    def reset_vector_store(self):
        #self.vector_store = InMemoryVectorStore(embedding=self.embeddings)
        index = faiss.IndexFlatL2(1536)  
        self.vector_store = FAISS(embedding_function=self.embeddings, index=index, docstore=InMemoryDocstore(), index_to_docstore_id={})
        self._last_used_id = 0


