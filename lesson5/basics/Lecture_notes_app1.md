# Python and Flask Basics 
     
## Introduction to Flask  
   
Flask is a Python micro-framework for web development. We use it to create web applications. In this example, a basic Flask app is created with several routes or URLs.  
   
## Understanding the Code  
   
```python  
from flask import Flask    
  
app = Flask(__name__)    
  
@app.route('/')    
def home():    
    return "Hello, this is a basic Flask app!"    
```  
In the above section, we first import the Flask module and create a Flask web server from the Flask module. `__name__` means this current file. We then define a route for the URL '/' which will trigger the function `home()`. This function returns the message "Hello, this is a basic Flask app!".  
   
```python  
@app.route('/page1')    
def page1():    
    message = "Hello, this is a basic Flask app!"  
    return f"""{message}<div></div>  
    <button><a href="/test-ai">Test AI</a></button> <br>  
    <a href="/test-ai">Test AI</a> <br>   
    <a href="/ask">Ask</a> <br>   
    <a href="/chat">Chat</a>"""  
```  
Here, we define another route '/page1'. The function `page1()` returns a string of HTML which includes the message variable and buttons linking to other pages.  
   
## HTML Template Example  
   
The following code shows an HTML template with a header, a button, an image, and a YouTube video.  
   
```python  
HTML_TEMPLATE = """  
<h1>Hello, this is a basic Flask app!</h1>    
<button><a href="/test-ai">Test AI</a></button> <br>    
<img src="https://placehold.co/200x200.png" alt="Placeholder Image"> <br>    
<iframe width="560" height="315" src="https://www.youtube.com/embed/CtdyoH-kvog?si=6lEVlWfIBuNhZhxy" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>   
"""  
@app.route('/page2')      
def page2():      
    return HTML_TEMPLATE  
```  
The route '/page2' will display this HTML when visited.  
   
## Using HTML Files   
  
```python  
from flask import Flask, render_template   
@app.route('/page3')      
def page3():      
    return render_template('home.html')     
```  
In this section, we return an HTML file `home.html` when the '/page3' route is visited. The `render_template()` function is used to generate output from a template file based on the Jinja2 engine that is found in the application's templates folder.  
   
## Running the Flask Application   
  
```python  
if __name__ == '__main__':    
    app.run(debug=True)  
```  
Finally, the Flask application is run with the `app.run()` method. We use `if __name__ == '__main__'` to make sure the app only runs if this script is the main program. The `debug=True` argument enables debug mode for the server.