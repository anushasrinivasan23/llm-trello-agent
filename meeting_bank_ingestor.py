# File: meetingbank_ingestor.py

import os
from datasets import load_dataset
from rag_pipeline import RAGPipeline

# Load MeetingBank dataset
meetingbank = load_dataset("huuuyeah/meetingbank")
train_data = meetingbank["train"]

# Create a folder to store txt files
os.makedirs("sample_docs", exist_ok=True)

# Save N transcripts from the dataset as txt files
N = 10  # Change as needed
file_paths = []

for item in train_data.select(range(N)):
    file_path = f"sample_docs/meeting_{item['id']}.txt"
    with open(file_path, "w") as f:
        f.write(item["transcript"])
    file_paths.append(file_path)

# Initialize and run the RAG pipeline
rag = RAGPipeline()
docs = rag.load_and_process_documents(file_paths)
rag.build_vectorstore(docs)

# Example query
from langchain_ollama import ChatOllama
llm = ChatOllama(model="mistral")

response = rag.run_query("What were the main issues discussed in the last meeting?", llm)
print("RAG Response:", response)
