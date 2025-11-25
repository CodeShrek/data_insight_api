# Data Insight API

A lightweight Data Analysis API built with Flask and OpenAI. This tool allows users to upload datasets (CSV, ZIP, or Text files) and ask natural language questions to extract insights, summary statistics, or specific data points without writing code.

## 🚀 Features

- **Natural Language Querying:** Ask questions in plain English (e.g., "What is the average value in column X?") and get precise answers.
- **Multi-Format Support:** Automatically handles and extracts data from:
  - **CSV Files:** Direct analysis of structured tabular data.
  - **ZIP Archives:** Automatically extracts and scans directories for relevant data files.
  - **Text Files:** Parses unstructured text content.
- **LLM Integration:** Leverages GPT-4 to interpret data schemas and generate intelligent responses.
- **RESTful Architecture:** Simple endpoint structure easy to integrate into frontend applications or automation workflows.

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **AI/LLM:** OpenAI API (GPT-4)
- **Data Processing:** Pandas, Zipfile
- **Environment:** Dotenv for secure configuration

## 📋 Prerequisites

- Python 3.8+
- An OpenAI API Key

## 🔧 Installation & Local Development

1. **Clone the repository**
   ```bash
   git clone [https://github.com/CodeShrek/data_insight_api.git](https://github.com/CodeShrek/data_insight_api.git)
   cd data_insight_api
