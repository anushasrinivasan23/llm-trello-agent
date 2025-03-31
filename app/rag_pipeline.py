from langchain.document_loaders import TextLoader, PyPDFLoader, Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

class RAGPipeline:
    def __init__(self, embedding_model=None):
        self.embedding_model = embedding_model or HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.vectorstore = None
        self.retriever = None
        self.qa_chain = None

    def load_and_process_documents(self, file_paths):
        documents = []
        for path in file_paths:
            if path.endswith(".txt"):
                loader = TextLoader(path)
            elif path.endswith(".pdf"):
                loader = PyPDFLoader(path)
            elif path.endswith(".docx"):
                loader = Docx2txtLoader(path)
            else:
                continue
            documents.extend(loader.load())

        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return splitter.split_documents(documents)

    def build_vectorstore(self, docs, llm):
        self.vectorstore = FAISS.from_documents(docs, embedding=self.embedding_model)
        self.retriever = self.vectorstore.as_retriever()
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=self.retriever,
            return_source_documents=True
        )

    def run_query(self, query):
        if not self.qa_chain:
            raise ValueError("QA chain not initialized.")
        result = self.qa_chain.invoke({"query": query})
        return result["result"]
