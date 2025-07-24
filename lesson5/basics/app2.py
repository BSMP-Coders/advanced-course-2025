from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# HTML template for the form
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Echo App</title>
</head>
<body>
    <h1>Interactive Echo App</h1>
    <form method="POST" action="/send_echo">
        <input type="text" name="message" placeholder="Enter your message">
        <input type="submit" value="Send to Echo Server">
    </form>
    {% if result %}
    <p>{{ result }}</p>
    {% endif %}
</body>
</html>
'''

def send_echo_request(message):
    url = "http://localhost:5000/echo"
    data = {"message": message}
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        print(f"Server responded: {response.json()['response']}")
        #return f"Server responded: {response.json()['response']}"
    else:
        return f"Error: Status code {response.status_code}"

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/send_echo', methods=['POST'])
def send_echo():
    message = request.form.get('message', '')
    result = send_echo_request(message)
    return render_template_string(HTML_TEMPLATE, result=result)

@app.route('/echo', methods=['POST'])
def echo():
    data = request.json
    message = data.get('message', 'No message sent')
    return jsonify({'response': message})

if __name__ == '__main__':
    app.run(debug=True)