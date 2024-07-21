# RAG Chatbot Application

![Bot Icon](bot-icon.png)
## Overview

Welcome to the Document RAG Chatbot Application! 
This project leverages the power of Retrieval-Augmented Generation via Large Language Model (LLM)
to create an intelligent chatbot capable of handling a wide range of queries, 
including those involving tables and images present in documents. Needless to say
it also handles your general LLM queries as well.

Aim is to create a full-fledged personal assistant bot capable of running in your local system. 
For now using LLM APIs which can be later converted to personal server calls once capable of 
hosting a good model in local!


## Features

- **Natural Language Understanding:** Accurately understands and responds to user queries.
- **Document Retrieval:** Retrieves relevant information from an unstructured corpus of documents.
- **Augmented Generation:** Enhances responses by combining retrieved information with generative capabilities.
- **Table Handling:** Processes and extracts data from tables in documents.
- **Image Handling:** Identifies and interprets images within documents.
- **Memory:** Chatbot has a limited context of previous chat history while you are having conversation with it. 

## Installation

1. **Clone the Repository:**
    ```bash
    git clone https://github.com/nnn007/document-rag.git
    cd document-RAG
    ```

2. **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Environment Variables:**
    - Create a `.env` file in the root directory.
      - Add necessary Gemini API keys.

## Usage

1. **Run the Application:**
    - First run the FastAPI backend server present in `main.py` file.
    ```bash
    python main.py
    ```
    - Then start the streamlit based chatbot application by giving this command:
    ```bash
    streamlit run app.py
    ```

2. **Interact with the Bot:**
    - Access the chatbot interface via the Streamlit app URL "http://localhost:8000" (can be changed based on your 
      convenience).
    - Start asking questions and receive intelligent responses!

## Contributing

We welcome contributions from the community! Please follow these steps:

1. **Fork the Repository**
2. **Create a New Branch**
    ```bash
    git checkout -b feature-branch
    ```
3. **Commit Your Changes**
    ```bash
    git commit -m "Add new feature"
    ```
4. **Push to the Branch**
    ```bash
    git push origin feature-branch
    ```
5. **Create a Pull Request**

   This app has a lot of scope of improvements and will be updating it in coming time so contributions are welcome! 
   Just putting up a basic implementation here. 

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please open an issue or reach out to me at [nayan.nilesh@gmail.com](mailto:nayan.nilesh@gmail.com).
