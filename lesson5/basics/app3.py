from flask import Flask, request, jsonify  
from openai import AzureOpenAI   
import os  
import dotenv    
  
dotenv.load_dotenv()    
  
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")    
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")    
MODEL_NAME = "gpt-35-turbo"  
  
app = Flask(__name__)   
  
openai_client = AzureOpenAI(api_key=AOAI_KEY,azure_endpoint=AOAI_ENDPOINT,api_version="2024-05-01-preview",)  
  
@app.route('/')    
def index():    
    return "Hello, this is a simple Flask server."   
  
@app.route('/chat', methods=['POST'])    
def chat():    
    data = request.get_json()    
    user_input = data.get('user_input', '')    

    response = openai_client.chat.completions.create(    
        model=MODEL_NAME,    
        messages=[    
            {"role": "system", "content": "You are a helpful assistant."},    
            {"role": "user", "content": user_input}    
        ],    
        max_tokens=50,    
        temperature=0.5    
    )    
    #return f"AI response: {response.choices[0].message.content}"
    suggestions = response.choices[0].message.content  
    return jsonify({'suggestions': suggestions})    
  

import requests

def send_chat_request(user_input):
    url = "http://localhost:5000/chat"
    data = {"user_input": user_input}
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        print(f"Server responded: {response.json()}")
    else:
        print(f"Error: Status code {response.status_code}")

# to test the chat function

if __name__ == '__main__':    
    app.run(debug=True)   
