import os
import zipfile
import json
import pandas as pd
import tempfile
import io
import google.generativeai as genai
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

# 2. Configure Gemini API
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print(" ERROR: GEMINI_API_KEY not found in .env file")
else:
    genai.configure(api_key=API_KEY)

app = Flask(__name__)
TEMP_DIR = tempfile.gettempdir()

def analyze_dataframe(df):
    """
    Generates a statistical summary of the data so the AI 
    understands the whole dataset, not just the top rows.
    """
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    
    # Create a rich summary
    summary = {
        "columns": df.columns.tolist(),
        "shape": df.shape, # (rows, columns)
        "column_types": str(df.dtypes.to_dict()),
        "missing_values": df.isnull().sum().to_dict(),
        "statistics": df.describe(include='all').to_dict(), # Mean, min, max, count
        "sample_data": df.head(20).to_dict(orient="records") # First 20 rows
    }
    return summary

def process_file(file):
    """Process uploaded file (ZIP, CSV, TXT) and extract insights."""
    if not file:
        return None
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(TEMP_DIR, filename)
    file.save(file_path)
    
    extracted_data = []
    
    try:
        # --- HANDLE ZIP FILES ---
        if filename.endswith('.zip'):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                extract_dir = os.path.join(TEMP_DIR, 'extracted')
                os.makedirs(extract_dir, exist_ok=True)
                zip_ref.extractall(extract_dir)
                
                # Walk through extracted files
                for root, _, files in os.walk(extract_dir):
                    for f_name in files:
                        full_path = os.path.join(root, f_name)
                        
                        # Process CSV inside ZIP
                        if f_name.endswith('.csv'):
                            try:
                                df = pd.read_csv(full_path)
                                extracted_data.append({
                                    "filename": f_name,
                                    "type": "csv",
                                    "analysis": analyze_dataframe(df)
                                })
                            except Exception as e:
                                extracted_data.append({"filename": f_name, "error": str(e)})
                        
                        # Process TXT inside ZIP
                        elif f_name.endswith('.txt'):
                            with open(full_path, 'r', encoding='utf-8') as f:
                                extracted_data.append({
                                    "filename": f_name, 
                                    "type": "text", 
                                    "content": f.read()[:10000] # Limit text size
                                })
                                
        # --- HANDLE DIRECT CSV ---
        elif filename.endswith('.csv'):
            df = pd.read_csv(file_path)
            extracted_data.append({
                "filename": filename,
                "type": "csv",
                "analysis": analyze_dataframe(df)
            })
            
        # --- HANDLE DIRECT TEXT ---
        elif filename.endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                extracted_data.append({
                    "filename": filename,
                    "type": "text",
                    "content": f.read()[:10000]
                })
                
        return extracted_data
    
    except Exception as e:
        return [{"error": f"File processing failed: {str(e)}"}]
    finally:
        # Cleanup uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)

def get_llm_response(question, file_data=None):
    """Send the question and data context to Gemini."""
    try:
        # --- CRITICAL CHANGE HERE ---
        # Using the model we confirmed is available in your list
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        # System Prompt
        prompt = (
            "You are an expert Data Analyst. "
            "I will provide you with a question and a summary of a dataset (including statistics, schema, and samples). "
            "Use the 'statistics' (mean, max, min) to answer aggregation questions accurately. "
            "Do NOT explain the process. Return ONLY the final answer value (number or string)."
            "\n\n"
        )
        
        prompt += f"USER QUESTION: {question}\n"
        
        if file_data:
            prompt += f"\nDATA CONTEXT:\n{json.dumps(file_data, indent=2)}\n"
            
        # Generate Answer
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        return f"AI Error: {str(e)}"

@app.route('/api/', methods=['POST'])
def solve_question():
    """Main API Endpoint"""
    try:
        # 1. Get Question
        question = request.form.get('question')
        if not question:
            return jsonify({"error": "No question provided"}), 400
        
        # 2. Process File (if provided)
        file_data = None
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:
                file_data = process_file(file)
        
        # 3. Ask Gemini
        answer = get_llm_response(question, file_data)
        
        return jsonify({"answer": answer})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({
        "status": "online", 
        "service": "Data Insight API (Gemini)",
        "model": "gemini-2.5-flash" # Updated label
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port)