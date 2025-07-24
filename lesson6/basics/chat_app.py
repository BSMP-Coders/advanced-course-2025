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