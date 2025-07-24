from openai import AzureOpenAI
import os
import requests  
import json

import dotenv  
# Load environment variables  
dotenv.load_dotenv()  # Put the keys and variables here (never put your real keys in the code)
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT_BSMP24")  
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY_BSMP24")  
MODEL_NAME = 'tts' #"gpt-35-turbo"

import requests  
import json  
  
# Define the endpoint and headers  
url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/tts/audio/speech?api-version=2024-02-15-preview"  
headers = {  
    "api-key": AZURE_OPENAI_API_KEY,  
    "Content-Type": "application/json"  
}  
  
# Define the data payload  
data = {  
    "model": "tts",#"tts-1-hd",  
    "input": "I'm excited to try text to speech.",  
    "voice": "alloy"  
}  
  
# Make the POST request  
response = requests.post(url, headers=headers, data=json.dumps(data))  
  
# Check if the request was successful  
if response.status_code == 200:  
    # Save the response content to a file  
    with open('speech.mp3', 'wb') as file:  
        file.write(response.content)  
    print("Audio saved as speech.mp3")  
else:  
    print(f"Request failed with status code {response.status_code}")  
    print(f"Response: {response.text}")  