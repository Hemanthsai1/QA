```markdown
# QA Bot Project

Welcome to the QA Bot Project! This project enables users to upload documents (PDF, TXT, CSV, PPTX, and DOCX) and ask questions based on the content of the uploaded documents. The bot retrieves relevant information and provides coherent answers.

 Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

 Features

- Upload multiple document types (PDF, TXT, CSV, PPTX, DOCX).
- Extract text from uploaded documents.
- Ask questions related to the document content.
- User-friendly interface with informative messages.

 Technologies Used

- Python
- Streamlit
- Cohere API / Hugging Face
- Weaviate
- Docker

 Setup Instructions

Prerequisites

1. Python 3.x: Ensure you have Python installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).

2. Install Required Libraries: Clone the repository and install the required libraries using pip. Open your terminal and run:

   ```bash
   git clone https://github.com/yourusername/qa-bot-project.git
   cd qa-bot-project
   pip install -r requirements.txt
   ```

3. API Keys: Obtain the necessary API keys for Cohere or Hugging Face and Weaviate. Store these keys in a `.env` file in the root directory of the project:

   ```plaintext
   COHERE_API_KEY=your_cohere_api_key
   WEAVIATE_API_KEY=your_weaviate_api_key
   WEAVIATE_URL=https://your-weaviate-cluster-url
   ```

 Usage

1. Run the Streamlit App: Start the application using the following command:

   ```bash
   streamlit run streamlit_app.py
   ```

2. Open the App: Navigate to `http://localhost:8501` in your web browser to access the QA bot interface.

3. Upload a Document: Click on the upload button to upload a document (PDF, TXT, CSV, PPTX, or DOCX).

4. Ask Questions: After the document is successfully uploaded, enter your questions in the provided text box. The bot will retrieve and display answers based on the document content.

 File Structure

```
qa-bot-project/
│
├── Dockerfile              # Docker configuration file
├── LICENSE                 # Project license
├── README.md               # Project documentation
├── __pycache__             # Compiled Python files
│   └── backend.cpython-311.pyc
├── backend.py              # Backend logic for the QA bot
├── codes                   # Folder for file handling modules
│   ├── __pycache__         # Compiled Python files for handling modules
│   │   ├── csv.cpython-311.pyc
│   │   ├── doc.cpython-311.pyc
│   │   └── ppt.cpython-311.pyc
│   ├── csv.py              # Logic for handling CSV files
│   ├── doc.py              # Logic for handling DOC files
│   └── ppt.py              # Logic for handling PPT files
├── main.py                 # Main entry point for the application
├── requirements.txt        # Required libraries
├── schema_setup.py         # Database schema setup
└── streamlit_app.py        # Streamlit app for user interface
```

 Contributing

Contributions are welcome! If you have suggestions for improvements or features, please create an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Push to the branch.
5. Create a pull request.

 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```