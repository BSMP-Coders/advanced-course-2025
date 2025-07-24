## Lesson 5: Flask Basics - Building a Simple Web App with ChatGPT Integration 🌐 

Similar to the lesson demo, we will be building a simple web application that integrates with Azure OpenAI's ChatGPT API. This time, we will be using Flask, a lightweight web framework for Python, to create the web app. In this folder you will find the following files:

- **app1.py:** A basic Flask app that responds with plain text.
- **app2.py:** A Flask app with a simple POST route that returns JSON responses.
  - **test_app2.py:** A test script for app2.py using the `requests` library.
- **app3.py:** A Flask app that integrates with Azure OpenAI to provide autocomplete suggestions.
  - **test_app3.py:** A test script for app3.py using the `requests` library.
- **app4.py:** app using Flask and OpenAI's ChatGPT API to provide autocomplete suggestion using HTML `chat_app4.html`.

Run the Flask apps using `python app1.py`, `python app2.py`, `python app3.py`, or `python app4.py`. You can test the apps by sending POST requests to the specified routes. When runninng `app2.py`, in a separate terminal, run `python test_app2.py` to test the POST route. When running `app3.py`, in a separate terminal, run `python test_app3.py` to test the autocomplete route.

### Part 1: Basic Flask App  
   
**Objective:** Get students familiar with Flask basics by creating a simple app that responds with plain text.  
   
**app1.py:**  
```python  
from flask import Flask  
   
app = Flask(__name__)  
   
@app.route('/')  
def home():  
    return "Hello, this is a basic Flask app!"  
   
if __name__ == '__main__':  
    app.run(debug=True)  
```  
   
**Explanation:**  
- **Flask Import:** Import the Flask class from the flask module.  
- **Create App:** Create an instance of the Flask class.  
- **Define Route:** Define a route (`/`) and a corresponding function (`home`) that returns a simple string.  
- **Run App:** Start the Flask application in debug mode.  
   
### Part 2: Adding a Simple POST Route  
   
**Objective:** Introduce the concept of handling POST requests and returning JSON responses.  
   
**app2.py:**  
```python  
from flask import Flask, request, jsonify  
   
app = Flask(__name__)  
   
@app.route('/')  
def home():  
    return "Hello, this is a basic Flask app!"  
   
@app.route('/echo', methods=['POST'])  
def echo():  
    data = request.json  
    message = data.get('message', 'No message sent')  
    return jsonify({'response': message})  
   
if __name__ == '__main__':  
    app.run(debug=True)  
```  
   
**Explanation:**  
- **Import request and jsonify:** Use `request` to get data from the client and `jsonify` to send JSON responses.  
- **Define POST Route:** Define a new route (`/echo`) that handles POST requests and returns the received message as a JSON response.  
   
### Part 3: Integrate with Azure OpenAI (without HTML)  
   
**Objective:** Show how to integrate with an external API (Azure OpenAI) and return its response.  
   
**app3.py:**  
```python  
from flask import Flask, request, jsonify  
from openai import AzureOpenAI  
import os  
import dotenv  
   
# Load environment variables  
dotenv.load_dotenv()  
   
# API keys and endpoints  
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")  
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")  
MODEL_NAME = "gpt-35-turbo"  
   
app = Flask(__name__)  
   
# Initialize OpenAI client  
openai_client = AzureOpenAI(api_key=AOAI_KEY, azure_endpoint=AOAI_ENDPOINT, api_version="2024-05-01-preview")  
   
@app.route('/')  
def home():  
    return "Hello, this is a basic Flask app!"  
   
@app.route('/autocomplete', methods=['POST'])  
def autocomplete():  
    data = request.json  
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
```  
   
**Explanation:**  
- **Environment Variables:** Use `dotenv` to load environment variables for API keys.  
- **Initialize OpenAI Client:** Create an instance of the AzureOpenAI client.  
- **Autocomplete Route:** Define a new route (`/autocomplete`) to handle POST requests and return suggestions from the OpenAI API.  
   
### Part 4: Adding Basic HTML (No JavaScript)  
   
**Objective:** Introduce HTML to display the response from the Flask app.  
   
**app4.py:**  
```python  
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
    return render_template('index.html')  
   
@app.route('/autocomplete', methods=['POST'])  
def autocomplete():  
    data = request.json  
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
```  
   
**templates/index.html:**  
```html  
<!DOCTYPE html>  
<html lang="en">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>Autocomplete</title>  
</head>  
<body>  
    <h1>Welcome to the Autocomplete App</h1>  
    <form action="/autocomplete" method="post">  
        <label for="inputText">Enter text:</label>  
        <input type="text" id="inputText" name="prompt">  
        <button type="submit">Submit</button>  
    </form>  
</body>  
</html>  
```  
   
**Explanation:**  
- **Render Template:** Use `render_template` to serve an HTML file.  
- **Basic HTML Form:** Create a simple form to submit a prompt to the `/autocomplete` route.  
   
### Part 5: Add JavaScript for Interactivity  
   
**Objective:** Introduce JavaScript to make the app more interactive.  
   
**app4.py:** (Same as Part 4)  
   
**templates/index.html:**  
```html  
<!DOCTYPE html>  
<html lang="en">  
<head>  
    <meta charset="UTF-8">  
    <meta name="viewport" content="width=device-width, initial-scale=1.0">  
    <title>Autocomplete</title>  
    <script>  
        async function getAutocomplete() {  
            const prompt = document.getElementById('inputText').value;  
            const response = await fetch('/autocomplete', {  
                method: 'POST',  
                headers: {  
                    'Content-Type': 'application/json'  
                },  
                body: JSON.stringify({ prompt })  
            });  
            const data = await response.json();  
            document.getElementById('suggestions').innerText = data.suggestions;  
        }  
    </script>  
</head>  
<body>  
    <h1>Welcome to the Autocomplete App</h1>  
    <div>  
        <input type="text" id="inputText" oninput="getAutocomplete()">  
        <div id="suggestions"></div>  
    </div>  
</body>  
</html>  
```  
   
**Explanation:**  
- **JavaScript Function:** Use JavaScript to make an asynchronous request to the Flask server and update the HTML with the response.  
   
By breaking it down into these parts, you can help your students understand each concept step-by-step.