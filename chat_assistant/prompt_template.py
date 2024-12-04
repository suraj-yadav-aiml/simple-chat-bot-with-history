from langchain_core.prompts import (
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    ChatPromptTemplate,
)


def initialize_prompt_template() -> ChatPromptTemplate:
    """
    Initializes the chat prompt template with system, user, and history placeholders.

    Returns:
        ChatPromptTemplate: A chat prompt template object.
    """
    system = SystemMessagePromptTemplate.from_template(template="You are a helpful AI Assistant.")
    human = HumanMessagePromptTemplate.from_template(template="{input}")
    messages = [system, MessagesPlaceholder(variable_name="history"), human]
    return ChatPromptTemplate.from_messages(messages=messages)
