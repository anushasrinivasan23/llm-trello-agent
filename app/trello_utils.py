from trello import TrelloClient

TRELLO_API_KEY = "YOUR_API_KEY"
TRELLO_TOKEN = "YOUR_TOKEN"
LIST_ID = "YOUR_LIST_ID"

client = TrelloClient(api_key=TRELLO_API_KEY, token=TRELLO_TOKEN)
trello_list = client.get_list(LIST_ID)

def create_trello_card(title, description):
    trello_list.add_card(title, description)
    print(f"✅ Task '{title}' added to Trello!")


# File: app/prompt_template.py
from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate(
    input_variables=["meeting_notes"],
    template="""
    You are an AI assistant specializing in workflow automation.
    Analyze the following meeting transcript and extract actionable tasks with assignees and priority levels.

    Meeting Notes:
    {meeting_notes}

    Format the output strictly as:
    1. [Task] - [Assignee] - [Priority]
    2. [Task] - [Assignee] - [Priority]
    3. [Task] - [Assignee] - [Priority]
    """
)