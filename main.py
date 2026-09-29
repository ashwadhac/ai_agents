from dotenv import load_dotenv
from langchain.agents import create_agent

from database import engine, Base
from tools import (
    add_todo,
    get_todos,
    complete_todo,
    delete_todo
)

load_dotenv()


# Create database tables
Base.metadata.create_all(bind=engine)


# Create AI Agent
agent = create_agent(
    model="google_genai:gemini-3.5-flash-lite",

    tools=[
        add_todo,
        get_todos,
        complete_todo,
        delete_todo
    ],

    system_prompt="""
    You are a helpful Todo AI Assistant.

    You can manage the user's todo list using the available tools.

    Available operations:
    - Add a todo
    - View todos
    - Complete a todo
    - Delete a todo

    Always use the appropriate tool when the user wants
    to perform an operation on their todo list.

    Be concise and friendly.
    """
)


print("Todo AI Agent started!")
print("Type 'exit' to stop.\n")


while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input
                }
            ]
        }
    )

    message = result["messages"][-1]

    if isinstance(message.content, list):
        print("AI:", message.content[0]["text"])
    else:
        print("AI:", message.content)