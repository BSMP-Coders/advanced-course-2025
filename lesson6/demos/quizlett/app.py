from flask import Flask, request, session, redirect, url_for, send_file
from openai import AzureOpenAI
import os
import dotenv  
# Load environment variables  
dotenv.load_dotenv()  
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")  
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")  
MODEL_NAME = "gpt-35-turbo"

AZURE_OPENAI_ENDPOINT_BSMP24 = os.getenv("AZURE_OPENAI_ENDPOINT_BSMP24")  
AZURE_OPENAI_API_KEY_BSMP24 = os.getenv("AZURE_OPENAI_API_KEY_BSMP24")  
MODEL_NAME = 'tts' #"gpt-35-turbo"

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")  # For session

openai_client = AzureOpenAI(
    api_key=AOAI_KEY,
    azure_endpoint=AOAI_ENDPOINT,
    api_version="2024-05-01-preview",
)


# Simple quiz questions (AI themed)
QUIZ_QUESTIONS = [
    {
        "question": "What does 'AI' stand for?",
        "answer": "artificial intelligence"
    },
    {
        "question": "Name one way AI can help make the world better.",
        "answer": None  # Open-ended
    },
    {
        "question": "Which company created Azure OpenAI?",
        "answer": "microsoft"
    }
]

def get_chat_history():
    return session.get('chat_history', [])

def add_to_chat(role, content):
    history = get_chat_history()
    history.append({"role": role, "content": content})
    session['chat_history'] = history

def get_quiz_state():
    return session.get('quiz_state', {"current": 0, "score": 0})

def set_quiz_state(state):
    session['quiz_state'] = state

@app.route('/', methods=['GET', 'POST'])
def quiz():
    quiz_state = get_quiz_state()
    chat_history = get_chat_history()
    current = quiz_state["current"]
    score = quiz_state["score"]

    if request.method == 'POST':
        user_answer = request.form.get('answer', '').strip().lower()
        add_to_chat("user", user_answer)
        # Check answer
        correct = False
        q = QUIZ_QUESTIONS[current]
        if q["answer"]:
            correct = user_answer == q["answer"].lower()
        else:
            correct = len(user_answer) > 0
        if correct:
            quiz_state["score"] += 1
            ai_reply = "Correct! "
        else:
            ai_reply = f"Not quite. The answer is: {q['answer'] if q['answer'] else 'Any good idea counts!'} "
        # LLM can elaborate
        prompt = f"{ai_reply} Next: {QUIZ_QUESTIONS[current+1]['question']}" if current+1 < len(QUIZ_QUESTIONS) else "Quiz finished!"
        response = openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a friendly AI quiz host for high school students. Theme: AI 4 Good."},
                *chat_history,
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        ai_message = response.choices[0].message.content
        add_to_chat("assistant", ai_message)
        quiz_state["current"] += 1
        set_quiz_state(quiz_state)
        return redirect(url_for('quiz'))

    # Start quiz or show next question
    if current >= len(QUIZ_QUESTIONS):
        end_message = f"Quiz complete! Your score: {score}/{len(QUIZ_QUESTIONS)}"
        return f"<h2>{end_message}</h2>" + render_chat(chat_history) + "<br><a href='/reset'>Restart Quiz</a>"
    question = QUIZ_QUESTIONS[current]["question"]
    if not chat_history:
        welcome = "Welcome to the AI 4 Good Quiz! Let's get started."
        add_to_chat("assistant", welcome)
    return render_chat(chat_history) + f'''
        <h3>Question {current+1}: {question}</h3>
        <form method="post">
            <input type="text" name="answer" autofocus>
            <input type="submit" value="Submit">
        </form>
        <form method="post" action="/tts">
            <button type="submit">🔊 Play last AI response</button>
        </form>
        <p>Score: {score}</p>
    '''

def render_chat(chat_history):
    html = "<div style='background:#f4f4f4;padding:10px;border-radius:8px;'>"
    for msg in chat_history:
        role = "<b>You:</b>" if msg["role"] == "user" else "<b>AI:</b>"
        html += f"<div>{role} {msg['content']}</div>"
    html += "</div>"
    return html

@app.route('/tts', methods=['POST'])
def tts():
    chat_history = get_chat_history()
    last_ai = next((msg['content'] for msg in reversed(chat_history) if msg['role'] == 'assistant'), None)
    if not last_ai:
        return "No AI message to convert to speech."    
    import requests, json
    url = f"{AZURE_OPENAI_ENDPOINT_BSMP24}/openai/deployments/tts/audio/speech?api-version=2024-02-15-preview"
    headers = {
        "api-key": AZURE_OPENAI_API_KEY_BSMP24,
        "Content-Type": "application/json"
    }
    data = {
        "model": "tts",
        "input": last_ai,
        "voice": "alloy"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        with open('speech.mp3', 'wb') as file:
            file.write(response.content)
        return send_file('speech.mp3', mimetype='audio/mpeg')
    else:
        return f"TTS failed: {response.text}", 500

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('quiz'))

if __name__ == '__main__':
    app.run(debug=True)