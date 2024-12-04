from langchain_community.chat_message_histories import SQLChatMessageHistory


class ChatHistoryManager:
    """
    Manages chat history stored in an SQLite database.
    """

    def __init__(self, db_connection: str):
        """
        Initializes the ChatHistoryManager with the database connection string.

        Args:
            db_connection (str): The SQLite connection string.
        """
        self.db_connection = db_connection

    def get_session_history(self, session_id: str) -> SQLChatMessageHistory:
        """
        Retrieves chat history for a specific session.

        Args:
            session_id (str): The session ID.

        Returns:
            SQLChatMessageHistory: The chat message history object.
        """
        return SQLChatMessageHistory(session_id=session_id, connection=self.db_connection)

    def get_user_messages(self, session_id: str) -> list:
        """
        Retrieves user chat messages.

        Args:
            session_id (str): The session ID.

        Returns:
            list: List of chat messages.
        """
        history = self.get_session_history(session_id)
        return history.get_messages()

    def clear_user_history(self, session_id: str) -> None:
        """
        Clears the chat history for a user.

        Args:
            session_id (str): The session ID.
        """
        history = self.get_session_history(session_id)
        history.clear()
