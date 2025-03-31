import os
import streamlit as st
from rag_pipeline import RAGPipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_ollama import ChatOllama

st.set_page_config(page_title="AI Task Agent with RAG")
st.title("AI Task Agent with RAG")

uploaded_file = st.file_uploader("Upload a meeting transcript (.txt)", type=["txt"])

mode = st.radio("Select Mode", ["Task Extraction", "Ask a Question (RAG)"])

if uploaded_file:
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"Uploaded `{uploaded_file.name}`")

    # Initialize
    rag = RAGPipeline()
    docs = rag.load_and_process_documents([file_path])

    llm = ChatOllama(model="mistral")
    rag.build_vectorstore(docs, llm)

    if mode == "Ask a Question (RAG)":
        user_query = st.text_input("Your question:")
        if user_query:
            try:
                response = rag.run_query(user_query)
                st.markdown("### Answer")
                st.write(response)
            except Exception as e:
                st.error(str(e))

    elif mode == "Task Extraction":
        try:
            prompt = PromptTemplate(
                input_variables=["context"],
                template="""
                Extract all action items from the meeting transcript below.
                Format them as a list like:
                1. Task - Assigned To - Deadline (if mentioned)

                Transcript:
                {context}
                """
            )

            context = "\n\n".join([doc.page_content for doc in docs])
            task_chain = LLMChain(llm=llm, prompt=prompt)
            extracted_tasks = task_chain.run(context)

            st.markdown("### Extracted Tasks")
            st.markdown(extracted_tasks)

            if st.button("Create Trello Cards"):
                from trello import TrelloClient

                # Make sure you have these env vars set
                client = TrelloClient(
                    api_key=os.getenv("TRELLO_API_KEY"),
                    api_secret=None,
                    token=os.getenv("TRELLO_TOKEN")
                )
                list_id = os.getenv("TRELLO_LIST_ID")
                trello_list = client.get_list(list_id)

                for line in extracted_tasks.strip().split("\n"):
                    if line.strip():
                        task = line.strip().split(" - ")[0]
                        trello_list.add_card(name=task)

                st.success("Trello cards created!")

        except Exception as e:
            st.error(str(e))
