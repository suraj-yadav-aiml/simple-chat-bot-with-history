# Simple Chat Bot with History

A simple and intuitive chatbot application built using **Streamlit** and **LangChain**. This chatbot allows users to chat with an AI assistant, and it maintains a chat history stored in a database for seamless conversations.

## Features

- **AI Chatbot**: Powered by LangChain's Ollama integration.
- **Chat History**: Maintains user-specific chat history using an SQLite database.
- **User-Friendly UI**: Built with Streamlit for a modern and attractive interface.
- **Customizable Settings**: Allows users to start new conversations and manage chat history.
- **Export Conversations**:
  - Download chat conversations as **text files** for offline storage.
  - Download chat conversations as **PDF files** with well-formatted structure,



## Directory Structure

```plaintext
project_directory/
│
├── chat_assistant/                   # Core logic for the chatbot
│   ├── __init__.py                   # Marks this directory as a package
│   ├── assistant.py                  # ChatAssistant class implementation
│   ├── config.py                     # Configuration constants like BASE_URL, MODEL, DB_CONNECTION
│   └── history.py                    # ChatHistoryManager class for managing history
|   └── expoter.py                    # ChatExporter class for downloading the conersations as text or pdf
│
├── streamlit_app/                    # Contains the Streamlit app files
│   ├── __init__.py                   # Optional, if multiple app modules are needed
│   ├── app.py                        # Main Streamlit app file
│
├── requirements.txt                  # Python dependencies for the project
└── README.md                         # Documentation for the project
```



## Prerequisites

1. **Python**: Ensure Python 3.8 or later is installed on your system.
2. **Ollama**: Install and set up Ollama for LangChain.

### How to Install Ollama

1. **Download Ollama**:  
   Visit the official [Ollama website](https://ollama.com/) and follow the instructions to download and install Ollama on your system.

2. **Start the Ollama Server**:  
   Once installed, start the Ollama server:
   ```bash
   ollama serve
   ```
   By default, the server will run at `http://localhost:11434`.

3. **Download a Model**:  
   Use the Ollama CLI to download a model. For example:
   ```bash
   ollama pull llama3.2
   ```
   This ensures the model is available for the chatbot.



## How to Run

### Step 1: Clone the Repository

Clone the project from GitHub:
```bash
git clone https://github.com/suraj-yadav-aiml/simple-chat-bot-with-history
cd simple-chat-bot-with-history
```

### Step 2: Install Dependencies

Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Step 3: Configure the Project

Update `chat_assistant/config.py` with the necessary settings:
- `BASE_URL`: Ensure it points to your Ollama server (e.g., `http://localhost:11434`).
- `MODEL`: Specify the name of the model you pulled (e.g., `llama3.2`).
- `DB_CONNECTION`: SQLite connection string (e.g., `sqlite:///chat_history.db`).

### Step 4: Run the Application

Navigate to the `streamlit_app/` directory and start the Streamlit app:
```bash
streamlit run app.py
```

### Step 5: Open in Browser

Once the app is running, open your browser and navigate to:
```plaintext
http://localhost:8501
```


## Usage

1. Enter your **User ID** in the sidebar.
2. Start chatting with the AI by typing messages in the input box.
3. View the chat history or start a new conversation using the sidebar controls.

## Future Improvements

Here are some ideas for enhancing the chatbot application:

1. **Advanced Model Selection**:  
   Add a feature in the sidebar to allow users to select from multiple AI models (e.g., GPT-4, Llama 2) dynamically during runtime.

2. **Export Chat History**:  
   Enable users to download their chat history as a text or PDF file for reference.

3. **Rich Media Responses**:  
   Enhance the assistant's responses to include images, graphs, or other media formats when applicable.

4. **Customizable Assistant Personality**:  
   Allow users to choose or configure the assistant's tone and personality (e.g., professional, friendly, humorous).

5. **Voice Input and Output**:  
    Integrate speech-to-text and text-to-speech capabilities to enable voice-based interaction with the chatbot.
---

## 🤝 **Contributing**
Contributions are welcome! Feel free to submit issues or pull requests.

