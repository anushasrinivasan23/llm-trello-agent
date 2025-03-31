# LLM-Trello-Agent

This project implements an AI-powered task automation assistant that performs question answering, task extraction, and Trello card creation from meeting transcripts using a locally deployed LLM.

## Features

- RAG-based question answering using Mistral 7B via Ollama
- Task extraction from meeting transcripts using prompt-based LLM chains
- Trello card creation from extracted action items
- Streamlit interface with two modes:
  - Ask a Question (RAG)
  - Task Extraction

## Tech Stack

- **Language Model**: Mistral 7B (via Ollama)
- **Frameworks**: LangChain, Streamlit
- **Embeddings**: SentenceTransformers
- **Vector Database**: FAISS
- **Automation**: Trello API

## Setup Instructions

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/llm-trello-agent.git
    cd llm-trello-agent
    ```

2. Create a virtual environment and activate it:
    ```bash
    conda create -n rag_agent_env python=3.11 -y
    conda activate rag_agent_env
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Start Ollama and pull the Mistral model:
    ```bash
    ollama run mistral
    ```

5. Launch the Streamlit app:
    ```bash
    streamlit run app/main.py
    ```

## Environment Variables

To enable Trello integration, set the following environment variables:

- `TRELLO_API_KEY`
- `TRELLO_TOKEN`
- `TRELLO_BOARD_ID`
- `TRELLO_LIST_ID`

You can add them to a `.env` file or export them in your shell.

## Directory Structure

```
llm-trello-agent/
├── app/
│   ├── main.py
│   ├── metrics.py
│   ├── rag_pipeline.py
│   ├── trello_utils.py
│── meeting_bank_ingestor.py
├── requirements.txt
└── README.md
```

## Output

- Direct answers to user queries
- List of extracted tasks
- Optional creation of Trello cards for tasks

## Demo
Watch a walkthrough of the AI Task Agent in action:
https://youtu.be/TOaJdto_JNY

## License

This project is licensed under the MIT License.
