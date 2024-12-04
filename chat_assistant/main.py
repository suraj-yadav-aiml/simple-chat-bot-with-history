from .config import BASE_URL, MODEL, DB_CONNECTION
from .assistant import ChatAssistant


def main():
    """
    Entry point for the chat assistant.
    """
    assistant = ChatAssistant(base_url=BASE_URL, model=MODEL, db_connection=DB_CONNECTION)
    session_id = "suraj-001"

    print("Chat Assistant is ready. Type 'x' to exit.")
    while True:
        try:
            question = input("Q: ")
            if question.lower() == "x":
                print("Exiting the chat. Goodbye!")
                break

            if not question.strip():
                print("Please enter a valid question.")
                continue

            answer = assistant.chat(session_id=session_id, user_input=question)
            print(f"A: {answer}")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
