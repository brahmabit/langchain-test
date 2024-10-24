import os
import json
from fastapi import UploadFile, HTTPException
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader, TextLoader
from langchain.docstore.document import Document as LangChainDocument
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain import hub
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

from app.utils.text import chunk_document
from app.api.services.helper.vector_store import VectorStoreSingleton
import traceback

from langchain_core.prompts import ChatPromptTemplate

system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

class VectorService:

    def __init__(self):
        #self.embeddings = OpenAIEmbeddings()
        #self.vector_store = InMemoryVectorStore(embedding=self.embeddings)
        self.vector_store = VectorStoreSingleton()

    def _load_pdf(self, file_path: str) -> LangChainDocument:
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        content = "\n".join([page.page_content for page in pages])  # Combine all pages
        return content, LangChainDocument(page_content=content)

    def _load_json(self, file_path: str) -> LangChainDocument:
        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            if isinstance(data, list):
                content = "\n".join(
                    "\n".join(f"{key}: {value}" for key, value in obj.items()) for obj in data
                )
            else:
                content = "\n".join(f"{key}: {value}" for key, value in data.items())
            return content, LangChainDocument(page_content=content)

        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON format: {e}")


    async def generate_embeddings(self, file_location: str) -> str:
        if file_location.endswith(".pdf"):
            content, document = self._load_pdf(file_location)
        elif file_location.endswith(".json"):
            content, document = self._load_json(file_location)
        else:
            raise HTTPException(
                status_code=400, detail=f"Unsupported file type: {file_location}"
            )
        metadata = {"filename": file_location.split("/")[-1]}
        #print(metadata)
        #Ideally we should split documets into smaller chunks
        #self.vector_store.add_documents(document, metadata)
        chunks = chunk_document(content)
        #self.vector_store.add_document_chunks(chunks, metadata)
        await self.vector_store.embed_chunks_in_batches(chunks, metadata)
        return f"File processed and stored successfully."
    
    async def answer_question_for_document(self, questions: list[str], filename: str = None):
        try:
            if filename:
                #NOTE: Dont use this for now, as it is not working
                #specific to a document
                #TODO: not working, check and correct
                retriever = self.vector_store.vector_store.as_retriever()
                retriever.search_kwargs["filter"] = {"filename": filename}
            else:
                #based on multiple documents
                retriever = self.vector_store.vector_store.as_retriever()
            llm = ChatOpenAI(model=os.getenv("OPEN_AI_MODEL", "gpt-4-1106-preview"), api_key=os.getenv("OPENAI_API_KEY"))
            question_answer_chain = create_stuff_documents_chain(llm, prompt)
            print(retriever)
            rag_chain = create_retrieval_chain(retriever, question_answer_chain)

            #results = rag_chain.invoke({"input": "What was Nike's revenue in 2023?"})
            response = []
            for q in questions:
                answer = rag_chain.invoke({"input": q})
                #print(answer['answer'])
                response.append({q: answer['answer']})

            self.vector_store.reset_vector_store()
            return response
        except Exception as e:
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"QnA failed: {str(e)}")


