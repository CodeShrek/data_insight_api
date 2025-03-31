# TDS Solver API

This API automatically answers questions from IIT Madras' Online Degree in Data Science Tools course graded assignments.

## Features

- Accepts questions from the 5 graded assignments
- Processes file attachments (ZIP, CSV, TXT)
- Returns answers in the required JSON format

## API Usage

Send a POST request to the API endpoint with your question and optional file attachment:

```bash
curl -X POST "https://your-app-url.vercel.app/api/" \
  -H "Content-Type: multipart/form-data" \
  -F "question=Download and unzip file abcd.zip which has a single extract.csv file inside. What is the value in the 'answer' column of the CSV file?" \
  -F "file=@abcd.zip"
```

The API will return a JSON response with the answer:

```json
{
  "answer": "1234567890"
}
```

## Local Development

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file with your OpenAI API key
6. Run the Flask application: `python app.py`

## Deployment

This API can be deployed to various platforms including Vercel, Heroku, and others.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.