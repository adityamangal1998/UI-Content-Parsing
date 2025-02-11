# Content Parsing and Q&A

This project is a Flask application that allows users to scrape content from URLs, store it in a vector database, and interact with the content through a chatbox. The application uses ChromaDB for storing and querying the content, and the Bedrock API for generating answers based on the scraped content.

## Features

- Scrape content from one or more URLs
- Store scraped content in ChromaDB
- Query the stored content using a chatbox
- Generate answers based on the stored content using the Bedrock API

## Requirements

- Python 3.7+
- Flask
- requests
- beautifulsoup4
- chromadb
- sentence-transformers
- boto3

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/UI-Content-Parsing.git
    cd UI-Content-Parsing
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure your AWS credentials and other settings in `config.py`:

    ```python
    # filepath: /d:/study/UI-Content-Parsing/config.py
    # AWS Configuration
    AWS_ACCESS_KEY_ID = 'your-aws-access-key-id'
    AWS_SECRET_ACCESS_KEY = 'your-aws-secret-access-key'
    AWS_REGION_NAME = 'your-aws-region'

    # Bedrock Model Configuration
    BEDROCK_MODEL_ID = 'your-bedrock-model-id'

    # ChromaDB Configuration
    CHROMA_DB_PATH = './chroma_db'
    CHROMA_COLLECTION_NAME = 'web_scraped_data'

    # Cross-Encoder Model
    CROSS_ENCODER_MODEL = 'cross-encoder/ms-marco-MiniLM-L-6-v2'

    # Embedding Model
    EMBEDDING_MODEL = 'BAAI/bge-base-en'
    ```

## Usage

1. Run the Flask application:

    ```bash
    python app.py
    ```

2. Open your web browser and navigate to `http://localhost:5000`.

3. Enter one or more URLs to scrape content and click "Scrape Content".

4. After the content is scraped and stored, enter a question in the chatbox and click "Get Answer" to receive an answer based on the stored content.

## Project Structure

```
/d:/study/UI-Content-Parsing
├── app.py
├── config.py
├── model.py
├── requirements.txt
├── static
│   ├── scripts.js
│   └── styles.css
├── templates
│   └── index.html
├── utils.py
└── vectordb.py
```

- `app.py`: Main Flask application file
- `config.py`: Configuration file for storing secret keys and other settings
- `model.py`: Contains the function to invoke the Bedrock API
- `requirements.txt`: List of required dependencies
- `static/`: Directory for static files (JavaScript and CSS)
- `templates/`: Directory for HTML templates
- `utils.py`: Utility functions for scraping content from URLs
- `vectordb.py`: Functions for storing and querying content in ChromaDB

## License

This project is licensed under the MIT License.
```