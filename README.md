#  Data Insight API (with Google Gemini)

A powerful, lightweight Data Analysis API built with Flask and Google Gemini. This tool empowers users to have a conversation with their data. Upload datasets (CSV, ZIP, or Text files) and ask natural language questions to instantly extract insights, perform calculations, and get specific data points without writing a single line of code.

## ⚙️ How It Works

The API follows a simple yet powerful workflow to turn your data and questions into clear answers.

1.  **Receive Request**: The Flask server accepts a `POST` request containing a natural language `question` and a `file`.
2.  **Process File**: The API intelligently detects the file type:
    *   **ZIP**: Extracts all contents and recursively finds and processes any `.csv` or `.txt` files within.
    *   **CSV**: Loads the data directly into a pandas DataFrame.
    *   **TXT**: Reads the text content.
3.  **Generate Statistical Summary**: For CSV files, it uses `pandas` to create a rich, statistical summary (schema, column types, mean, min, max, missing values, etc.). This pre-analysis is crucial for giving the AI deep context.
4.  **Construct Prompt**: It builds a detailed prompt for Google Gemini, combining your question with the file content or the statistical summary. The prompt is engineered to request a direct, clean answer.
5.  **Get Answer**: The request is sent to the Gemini API, which returns a precise, data-driven answer.
6.  **Return JSON**: The final answer is sent back to the user in a clean JSON format.

##  Features

- **Natural Language Querying:** Ask questions in plain English (e.g., "What is the average value in column X?") and get precise answers.
- **Multi-Format Support:** Automatically handles and extracts data from:
  - **CSV Files:** Direct analysis of structured tabular data.
  - **ZIP Archives:** Automatically extracts all contents, finds supported files (`.csv`, `.txt`), and includes them in the analysis context.
  - **Text Files:** Parses and analyzes unstructured text content.
- **Intelligent Data Summarization:** Before querying the AI, the API first uses `pandas` to generate a rich statistical summary of your data (schema, column types, mean, min, max, null values, etc.). This provides the AI with crucial context for more accurate and efficient analysis.
- **LLM Integration:** Leverages **Google Gemini** to understand the data's structure and your question, providing intelligent and context-aware responses.
- **Simple RESTful Architecture:** A clean, single-endpoint design that is easy to integrate into any frontend application, script, or automation workflow (like Postman).

##  Use Cases

- **Interactive Data Chatbots**: Build a user-friendly chatbot that allows non-technical users to query company data.
- **Automated Reporting**: Integrate the API into a script to automatically generate daily summaries or answer recurring business questions.
- **Data Exploration for Analysts**: Quickly get high-level statistics or validate hypotheses without writing complex scripts.
- **Educational Tools**: Create applications that help students learn data analysis concepts by interacting with datasets in natural language.

##  Tech Stack

- **Backend:** Python, Flask
- **AI/LLM:** Google Gemini API (`gemini-1.5-flash`)
- **Data Processing:** Pandas
- **Environment:** Python-Dotenv for secure API key management

## 📋 Prerequisites

- Python 3.8+
- A **Google Gemini API Key**. You can get one from Google AI Studio.

##  Installation & Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/CodeShrek/data_insight_api.git
   cd data_insight_api
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   # On Windows, use: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your API Key**
   - Create a file named `.env` in the root of the project directory.
   - Add your Google Gemini API key to this file:
     ```
     GEMINI_API_KEY="YOUR_API_KEY_HERE"
     ```

5. **Run the application**
   ```bash
   python app.py
   ```
   The API will be running at `http://127.0.0.1:8000`.

## ⚙️ API Endpoints

### 1. Health Check

Confirms that the service is online.

- **Endpoint:** `/`
- **Method:** `GET`
- **Success Response (200):**
  ```json
  {
    "status": "online",
    "service": "Data Insight API (Gemini)",
    "model": "gemini-1.5-flash"
  }
  ```

### 2. Analyze Data

The core endpoint for uploading a file and asking a question.

- **Endpoint:** `/api/`
- **Method:** `POST`
- **Body:** `form-data`
  - `question` (text): The question you want to ask about the data.
  - `file` (file): The dataset file (`.csv`, `.zip`, `.txt`).

- **Success Response (200):**
  ```json
  {
    "answer": "The calculated result from the AI"
  }
  ```

- **Error Response (400):**
  ```json
  {
    "error": "No question provided"
  }
  ```

#### Example `curl` Request

**Example 1: Calculating an average**

```bash
curl -X POST http://127.0.0.1:8000/api/ \
  -F "question=What is the average age of all people in the file?" \
  -F "file=@sample_data.csv"
```

**Expected Output:**
```json
{
  "answer": "30"
}
```


You can also view live Demo on - https://codeshrek.pythonanywhere.com/
this site is functional till-   Saturday 28 February 2026




## ENJOY
