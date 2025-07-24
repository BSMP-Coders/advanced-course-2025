from flask import Flask  
  
app = Flask(__name__)  
  
@app.route('/')  
def home():  
    return "Hello, this is a basic Flask app!"  

@app.route('/page1')  
def page1():  
    message = "Hello, this is a basic Flask app!"
    # Return a page that links to these three pages /test-ai, /ask, /chat
    return f"""{message}<div></div>
    <button><a href="/test-ai">Test AI</a></button> <br>
    <a href="/test-ai">Test AI</a> <br> 
                <a href="/ask">Ask</a> <br> 
                <a href="/chat">Chat</a>"""



# HTML TEMPLATE (show examples on how to do basic buttons, images, video, images in columns for images just use https://placehold.co/200x200.png for the video use https://youtu.be/CtdyoH-kvog?si=Kgf6VjLLR-h0YD3n)

HTML_TEMPLATE = """
<h1>Hello, this is a basic Flask app!</h1>  
<button><a href="/test-ai">Test AI</a></button> <br>  
<img src="https://placehold.co/200x200.png" alt="Placeholder Image"> <br>  
<iframe width="560" height="315" src="https://nfl24cdn.azureedge.net/nflblob/bsmp25/bsmp_proj_vids/PdfBrainstorm_720p.mp4" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe> 
"""
@app.route('/page2')    
def page2():    
    return HTML_TEMPLATE


from flask import Flask, render_template 
@app.route('/page3')    
def page3():    
    return render_template('home.html')   

if __name__ == '__main__':  
    app.run(debug=True)  