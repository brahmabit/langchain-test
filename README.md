
## Features  
**Independent APIs**  
   - **Document Upload**: Upload a document for processing.  
   - **QnA API**: Submit questions to get answers based on previously uploaded documents.  
**Combined API**  
   - Upload documents and questions simultaneously, and receive answers in one operation.

## API Endpoints  

### **Combined API**  
Uploads both a document and a question file, returning the answer in a single call.  Relevant API 

```bash
curl --location 'http://localhost:8000/v1/qna/upload-file-question-file-answer' \
--form 'question_file=@"/Users/brahmabit/Documents/LANGCHAIN/langchain-test/sample/question/question_json.json"' \
--form 'document_file=@"/Users/brahmabit/Documents/LANGCHAIN/langchain-test/sample/doc/posts_1.json"' \
--form 'download_as_file="false"'
```

### **Document Upload API**  
Uploads a document to the server for future queries.  

```bash
curl --location 'http://localhost:8000/v1/file/upload' \
--form 'files=@"/Users/brahmabit/Downloads/posts.json"'
```

### **QnA API**  
Submits a list of questions to get answers based on the uploaded documents.

```bash
curl --location 'http://localhost:8000/v1/qna/question' \
--header 'Content-Type: application/json' \
--data '{
    "questions": [
        "What is the document about?",
        "How many blogs are there?",
        "Which is the most read blog?",
        "Anything interesting in the blog?"
    ]
}'
```

## Current Major Limitation  
- **Document Filtering**:  
  - The system cannot distinguish between individual documents within the vector store. If multiple documents are uploaded, responses may mix content from different files.



## Possible Extensions  
1. **Proper Vector Store DB**:    
2. **Auth**:  
3. **Logging and monitoring**:  
4. **Database integration**:  
5. **Using proper interfaces(pydantic models)**
6. **Proper test cases**



### Installation  

1. Clone the repository:
   ```bash
   git clone repo
   cd repo
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in .env file:
   
    - OPENAI_API_KEY=
    - OPEN_AI_MODEL=
   

4. Run the server:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```


## Usage  

**Combined Usage**  
   Use the **Combined API** to upload a document and submit questions simultaneously. This is the question realted endpoint. It has and attribute to either get JSON response or download as octet-stream "download_as_file"


