
# LLM Quiz App

![](/demos/quizlett/image.png)



Your Flask app now supports a conversational AI quiz game for high school students, themed “AI 4 Good.” It tracks chat history, quiz progress, and score. Users can play the last AI response as audio using the TTS button, which calls your Azure TTS API.

- The home page welcomes users and starts the quiz.
- Each question is conversational, and the LLM responds to answers.
- The TTS button lets users hear the last AI message.
- The UI shows chat history, current question, score, and a restart option.

You can further customize questions, voices, or add more features as needed. Let me know if you want to improve the UI or add more quiz logic!

----

Here is all the code in your workspace relevant to your request for a basic quiz Flask LLM app with text-to-speech (TTS) functionality, a conversational interface, and a button for users to trigger TTS (for a podcast quiz game/AI demo):

---

**1. LLM Flask App Example (`app.py`):**
This file contains a basic Flask app using Azure OpenAI for conversational AI. It demonstrates how to set up a form for user input and return an AI-generated response.

```python
from flask import Flask, request
from openai import AzureOpenAI
import os
import dotenv  
# Load environment variables  
dotenv.load_dotenv()  
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")  
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")  
MODEL_NAME = "gpt-35-turbo"

app = Flask(__name__)

openai_client = AzureOpenAI(
    api_key=AOAI_KEY,
    azure_endpoint=AOAI_ENDPOINT,
    api_version="2024-05-01-preview",
)

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        prompt = request.form.get('prompt', '')
        response = openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50
        )
        return f"AI response: {response.choices[0].message.content}"
    return '''
        <form method="post">
            <input type="text" name="prompt">
            <input type="submit" value="Ask AI">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
```

---

**2. Text-to-Speech Example (`tts_api.py`):**
This file shows how to use Azure OpenAI's TTS API to convert text to speech and save the result as an audio file. This can be adapted to run when a user clicks a button in your Flask app.

```python
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
```

---

**3. Environment Variables Example (`.env-sample`):**
Shows the required environment variables for both LLM and TTS endpoints and keys.

```
AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_API_KEY=""

# BSMP4
AZURE_OPENAI_ENDPOINT_BSMP24 =""
AZURE_OPENAI_API_KEY_BSMP24 =""
```

---

**4. Requirements (`requirements.txt`):**
Lists the required Python packages for Flask, OpenAI, TTS, and environment variable management.

```
openai>=1.0.0,<2.0.0
python-dotenv
Flask==3.0.3
requests
chess
python-chess
```

---

**Summary of Relevant Concepts:**
- Conversational LLM Flask app (app.py)
- TTS API usage (tts_api.py)
- Environment variable setup (.env-sample)
- Required dependencies (requirements.txt)

You can combine the conversational LLM logic from `app.py` with the TTS logic from `tts_api.py`, and add a button in your Flask app to trigger TTS for the AI's response, creating an interactive podcast quiz game for your AI demo.Here’s a plan for your basic conversational quiz Flask LLM app with TTS integration:

**Features:**
- Home page: Welcomes user, explains the quiz, and starts the conversation.
- Quiz flow: User answers questions, LLM evaluates and responds, tracks score.
- TTS: Button to play the last AI response as audio (using your TTS API).
- Conversational: Each interaction is part of a chat history.
- Theme: “AI 4 Good” and learning about AI.

**Implementation Steps:**
1. Update app.py to:
   - Add a conversational quiz flow (track questions, answers, score, chat history).
   - Add a button to trigger TTS for the last AI message.
   - Use Flask session to store chat history and quiz state.
2. Add TTS endpoint in Flask to call your TTS API and serve the audio file.
3. Update HTML to show chat history, quiz questions, answer form, and TTS button.

I’ll start by updating app.py to implement the conversational quiz logic, TTS endpoint, and improved UI. 
```


Made changes.


```
Your Flask app now supports a conversational AI quiz game for high school students, themed “AI 4 Good.” It tracks chat history, quiz progress, and score. Users can play the last AI response as audio using the TTS button, which calls your Azure TTS API.

- The home page welcomes users and starts the quiz.
- Each question is conversational, and the LLM responds to answers.
- The TTS button lets users hear the last AI message.
- The UI shows chat history, current question, score, and a restart option.

You can further customize questions, voices, or add more features as needed. Let me know if you want to improve the UI or add more quiz logic!



Here is all the code in your workspace relevant to your request for a basic quiz Flask LLM app with text-to-speech (TTS) functionality, a conversational interface, and a button for users to trigger TTS (for a podcast quiz game/AI demo):

---

**1. LLM Flask App Example (`app.py`):**
This file contains a basic Flask app using Azure OpenAI for conversational AI. It demonstrates how to set up a form for user input and return an AI-generated response.

```python
from flask import Flask, request
from openai import AzureOpenAI
import os
import dotenv  
# Load environment variables  
dotenv.load_dotenv()  
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")  
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")  
MODEL_NAME = "gpt-35-turbo"

app = Flask(__name__)

openai_client = AzureOpenAI(
    api_key=AOAI_KEY,
    azure_endpoint=AOAI_ENDPOINT,
    api_version="2024-05-01-preview",
)

@app.route('/', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        prompt = request.form.get('prompt', '')
        response = openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50
        )
        return f"AI response: {response.choices[0].message.content}"
    return '''
        <form method="post">
            <input type="text" name="prompt">
            <input type="submit" value="Ask AI">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
```

---

**2. Text-to-Speech Example (`tts_api.py`):**
This file shows how to use Azure OpenAI's TTS API to convert text to speech and save the result as an audio file. This can be adapted to run when a user clicks a button in your Flask app.

```python
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
```

---

**3. Environment Variables Example (`.env-sample`):**
Shows the required environment variables for both LLM and TTS endpoints and keys.

```
AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_API_KEY=""

# BSMP4
AZURE_OPENAI_ENDPOINT_BSMP24 =""
AZURE_OPENAI_API_KEY_BSMP24 =""
```

---

**4. Requirements (`requirements.txt`):**
Lists the required Python packages for Flask, OpenAI, TTS, and environment variable management.

```
openai>=1.0.0,<2.0.0
python-dotenv
Flask==3.0.3
requests
chess
python-chess
```

---

**Summary of Relevant Concepts:**
- Conversational LLM Flask app (app.py)
- TTS API usage (tts_api.py)
- Environment variable setup (.env-sample)
- Required dependencies (requirements.txt)

You can combine the conversational LLM logic from `app.py` with the TTS logic from `tts_api.py`, and add a button in your Flask app to trigger TTS for the AI's response, creating an interactive podcast quiz game for your AI demo.Here’s a plan for your basic conversational quiz Flask LLM app with TTS integration:

**Features:**
- Home page: Welcomes user, explains the quiz, and starts the conversation.
- Quiz flow: User answers questions, LLM evaluates and responds, tracks score.
- TTS: Button to play the last AI response as audio (using your TTS API).
- Conversational: Each interaction is part of a chat history.
- Theme: “AI 4 Good” and learning about AI.

**Implementation Steps:**
1. Update app.py to:
   - Add a conversational quiz flow (track questions, answers, score, chat history).
   - Add a button to trigger TTS for the last AI message.
   - Use Flask session to store chat history and quiz state.
2. Add TTS endpoint in Flask to call your TTS API and serve the audio file.
3. Update HTML to show chat history, quiz questions, answer form, and TTS button.

I’ll start by updating app.py to implement the conversational quiz logic, TTS endpoint, and improved UI. 
```


Made changes.


```
