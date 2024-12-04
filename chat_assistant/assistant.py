from langchain_ollama import ChatOllama
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.output_parsers import StrOutputParser
from .history import ChatHistoryManager
from .prompt_template import initialize_prompt_template
from typing import Dict


class ChatAssistant:
    """
    Manages interaction with a LangChain-based LLM.
    """

    def __init__(self, base_url: str, model: str, db_connection: str):
        """
        Initializes the ChatAssistant.

        Args:
            base_url (str): The base URL for the LLM API.
            model (str): The model name to use.
            db_connection (str): The SQLite connection string for history management.
        """
        self.base_url = base_url
        self.model = model
        self.history_manager = ChatHistoryManager(db_connection)
        self.llm = ChatOllama(base_url=base_url, model=model)
        self.template = initialize_prompt_template()
        self.chain = self.template | self.llm | StrOutputParser()
        self.runnable_with_history = RunnableWithMessageHistory(
            runnable=self.chain,
            get_session_history=self.history_manager.get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )

    def chat(self, session_id: str, user_input: str) -> str:
        """
        Interacts with the LLM using user input.

        Args:
            session_id (str): The session ID.
            user_input (str): The user input message.

        Returns:
            str: The LLM's response.
        """
        try:
            response = self.runnable_with_history.invoke(
                input={"input": user_input},
                config={"configurable": {"session_id": session_id}},
            )
            return response
        except Exception as e:
            raise RuntimeError(f"Failed to process chat request: {e}")
