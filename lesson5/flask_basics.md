# Introduction to Flask

## Overview

Welcome to your next adventure in web development! So far, you've been building web apps using Streamlit. Now, we're going to explore Flask, another powerful tool for creating web applications. This guide will help you understand the differences between Streamlit and Flask and get you started with Flask basics.

## What's the Difference Between Streamlit and Flask?

### Streamlit:
- **Purpose**: Streamlit is designed for quickly building interactive web apps for data science and machine learning.
- **Ease of Use**: It's very easy to use and you can create apps with just a few lines of Python code.
- **Features**: Streamlit takes care of most of the web development for you. It automatically handles the front end (what users see) and the back end (the logic and data processing).

### Flask:
- **Purpose**: Flask is a web framework used to build more general web applications. It gives you more control over your app's structure and behavior.
- **Flexibility**: Flask requires more setup and code, but it also gives you more flexibility and control.
- **Client-Server Model**: Flask follows a client-server model, where the client (browser) makes requests to the server (your Flask app) which processes these requests and sends back responses (like web pages or data).

## Getting Started with Flask

### Basic Concepts

- **Client**: The client is what the user interacts with, usually a web browser.
- **Server**: The server processes requests from the client and sends back responses. In Flask, you'll write Python code to define how the server handles these requests.
- **Routes**: Routes in Flask are like addresses that point to different parts of your web app. Each route is associated with a specific function in your code that defines what should happen when someone visits that route.

### Setting Up Flask

1. **Install Flask**:
   Open your terminal or command prompt and run:
   ```bash
   pip install flask
   ```

2. **Create a Simple Flask App**:
   Create a new file called `app.py` and add the following code:
   ```python
   from flask import Flask

   app = Flask(__name__)

   @app.route('/')
   def home():
       return "Hello, Flask!"

   if __name__ == '__main__':
       app.run(debug=True)
   ```

3. **Run Your Flask App**:
   In your terminal or command prompt, navigate to the directory where `app.py` is located and run:
   ```bash
   python app.py
   ```
   Open your web browser and go to `http://127.0.0.1:5000/` to see your app in action.


### Next Steps

In the next lesson, we'll dive deeper into Flask by building a more interactive web app that integrates with GPT using the Azure OpenAI API. You'll learn how to handle user input, display dynamic content, and make your Flask app communicate with an AI model.

### Additional Resources

For a more detailed introduction to Flask, you can refer to the [LaunchCode Education Flask Guide](https://education.launchcode.org/lchs/chapters/flask-intro/first-flask-app.html).

Happy coding! 🚀
