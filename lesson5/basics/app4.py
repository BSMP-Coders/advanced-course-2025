from flask import Flask, request, jsonify, render_template  
from openai import AzureOpenAI  
import os  
import dotenv  
  
dotenv.load_dotenv()  
  
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")  
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")  
MODEL_NAME = "gpt-35-turbo"  
  
app = Flask(__name__)  
  
openai_client = AzureOpenAI(api_key=AOAI_KEY, azure_endpoint=AOAI_ENDPOINT, api_version="2024-05-01-preview")  
  
@app.route('/')  
def home():  
    return render_template('chat_app4.html')  
  
@app.route('/autocomplete', methods=['POST'])  
def autocomplete():  
    data = request.get_json()  
    prompt = data.get('prompt', '')  
    response = openai_client.chat.completions.create(  
        model=MODEL_NAME,  
        messages=[  
            {"role": "system", "content": "You are an autocomplete assistant."},  
            {"role": "user", "content": prompt}  
        ],  
        max_tokens=50,  
        temperature=0.5  
    )  
    suggestions = response.choices[0].message.content  
    return jsonify({'suggestions': suggestions})  
  
if __name__ == '__main__':  
    app.run(debug=True)  
