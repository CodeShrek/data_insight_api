import os
import zipfile
import json
import pandas as pd
import tempfile
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

# Set up temporary directory for file processing
TEMP_DIR = tempfile.gettempdir()

def process_file(file):
    """Process uploaded file and extract relevant information."""
    if not file:
        return None
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(TEMP_DIR, filename)
    
    # Save the file temporarily
    file.save(file_path)
    
    file_content = None
    file_info = {
        "filename": filename,
        "content": None
    }
    
    try:
        # Process ZIP files
        if filename.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Extract all files to temporary directory
                extract_dir = os.path.join(TEMP_DIR, 'extracted')
                os.makedirs(extract_dir, exist_ok=True)
                zip_ref.extractall(extract_dir)
                
                # Process extracted files
                extracted_files = []
                for root, dirs, files in os.walk(extract_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        if file.endswith('.csv'):
                            try:
                                df = pd.read_csv(file_path)
                                file_info["content"] = {
                                    "type": "csv",
                                    "columns": df.columns.tolist(),
                                    "sample": df.head(5).to_dict(orient="records"),
                                    "shape": df.shape
                                }
                                
                                # Check if 'answer' column exists
                                if 'answer' in df.columns:
                                    file_info["answer_column"] = df['answer'].tolist()
                                
                                extracted_files.append(file_info)
                            except Exception as e:
                                extracted_files.append({
                                    "filename": file,
                                    "error": str(e)
                                })
                        elif file.endswith('.txt'):
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                extracted_files.append({
                                    "filename": file,
                                    "type": "text",
                                    "content": content
                                })
                return extracted_files
        
        # Process CSV files directly
        elif filename.endswith('.csv'):
            df = pd.read_csv(file_path)
            file_info["content"] = {
                "type": "csv",
                "columns": df.columns.tolist(),
                "sample": df.head(5).to_dict(orient="records"),
                "shape": df.shape
            }
            
            # Check if 'answer' column exists
            if 'answer' in df.columns:
                file_info["answer_column"] = df['answer'].tolist()
            
            return [file_info]
        
        # Process text files
        elif filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                file_info["content"] = {
                    "type": "text",
                    "content": content
                }
            return [file_info]
        
        else:
            file_info["content"] = {
                "type": "unknown",
                "message": "Unsupported file type"
            }
            return [file_info]
    
    except Exception as e:
        return [{
            "filename": filename,
            "error": str(e)
        }]
    finally:
        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)

def get_llm_response(question, file_data=None):
    """Get response from LLM based on the question and file data."""
    try:
        # Prepare the message for the LLM
        messages = [
            {"role": "system", "content": "You are an AI assistant helping with data science assignments. Your task is to provide precise, concise answers to questions. If the question involves analyzing data from a file, extract the exact answer requested. Return only the answer value, with no explanations or additional text."}
        ]
        
        # Add the question
        user_message = f"Question: {question}\n"
        
        # Add file data if available
        if file_data:
            user_message += f"\nFile data: {json.dumps(file_data, indent=2)}\n"
        
        user_message += "\nPlease provide ONLY the answer value, with no explanations. The answer should be in a format that can be directly entered into an assignment submission field."
        
        messages.append({"role": "user", "content": user_message})
        
        # Get response from OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or another appropriate model
            messages=messages
        )
        
        # Extract the answer from the response
        answer = response.choices[0].message['content'].strip()
        return answer
    
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/api/', methods=['POST'])
def solve_question():
    """Main API endpoint to process questions and return answers."""
    try:
        # Get the question from the request
        question = request.form.get('question')
        if not question:
            return jsonify({"error": "No question provided"}), 400
        
        # Check if a file was uploaded
        file_data = None
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:  # Check if a file was actually selected
                file_data = process_file(file)
        
        # Get answer from LLM
        answer = get_llm_response(question, file_data)
        
        # Return the answer in the required format
        return jsonify({"answer": answer})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Add a simple health check endpoint
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "TDS Solver API is running"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)