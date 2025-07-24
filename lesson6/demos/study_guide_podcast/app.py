from flask import Flask, request, session, redirect, url_for, send_file, render_template_string
from openai import AzureOpenAI
import os
import dotenv
import requests, json
from PIL import Image
from io import BytesIO

# Load environment variables
dotenv.load_dotenv()
AOAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AOAI_KEY = os.getenv("AZURE_OPENAI_API_KEY")
MODEL_NAME = "gpt-35-turbo"

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "supersecretkey")

openai_client = AzureOpenAI(
    api_key=AOAI_KEY,
    azure_endpoint=AOAI_ENDPOINT,
    api_version="2024-05-01-preview",
)

def get_chat_history():
    return session.get('chat_history', [])

def add_to_chat(role, content):
    history = get_chat_history()
    history.append({"role": role, "content": content})
    session['chat_history'] = history

def get_uploaded_text():
    return session.get('uploaded_text', None)

@app.route('/', methods=['GET', 'POST'])
def study_guide():
    chat_history = get_chat_history()
    uploaded_text = get_uploaded_text()
    ai_message = None
    dalle_image_path = session.get('dalle_image_path')

    if request.method == 'POST' and 'question' in request.form:
        question = request.form.get('question', '').strip()
        add_to_chat("user", question)
        # Use uploaded text as context
        context = uploaded_text if uploaded_text else "No study guide uploaded yet."
        prompt = f"Here is the study guide:\n{context}\n\nAnswer the user's question conversationally: {question}"
        response = openai_client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a friendly AI tutor for high school students. Theme: AI 4 Good."},
                *chat_history,
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        ai_message = response.choices[0].message.content
        add_to_chat("assistant", ai_message)
        return redirect(url_for('study_guide'))

    # Render chat and UI, including DALL-E image if available
    html = render_chat(chat_history)
    html += '''
        <h2>Study Guide Podcast App</h2>
        <form method="post" enctype="multipart/form-data" action="/upload">
            <input type="file" name="file" accept=".txt">
            <input type="submit" value="Upload Study Guide">
        </form>
        <form method="post">
            <input type="text" name="question" placeholder="Ask a question about your study guide" autofocus>
            <input type="submit" value="Ask AI">
        </form>
        <button id="ttsBtn">🔊 Play last AI response & Generate Image</button>
        <button id="demoBtn">▶️ Replay Demo</button>
        <audio id="ttsAudio" controls style="display:none;margin-top:10px;"></audio>
        <audio id="demoAudio" controls style="display:none;margin-top:10px;"></audio>
        <div id="dalleImageContainer">
    '''
    if dalle_image_path:
        html += f'<h3>AI Generated Image:</h3><img src="{dalle_image_path}" alt="AI Image" style="max-width:400px;border-radius:8px;">'
    html += '''</div>
        <div id="demoChatContainer"></div>
        <div id="demoImageContainer"></div>
        <br><a href="/reset">Reset Session</a>
        <script>
        document.getElementById('ttsBtn').onclick = async function(e) {
            e.preventDefault();
            const btn = document.getElementById('ttsBtn');
            btn.disabled = true;
            btn.textContent = 'Generating...';
            try {
                const response = await fetch('/tts', {method: 'POST'});
                if (response.ok) {
                    const blob = await response.blob();
                    const audioUrl = URL.createObjectURL(blob);
                    const audio = document.getElementById('ttsAudio');
                    audio.src = audioUrl;
                    audio.style.display = 'block';
                    audio.play();
                } else {
                    alert('TTS failed.');
                }
                // Always try to fetch the image path, even if TTS fails
                const imgResp = await fetch('/dalle_image_path');
                if (imgResp.ok) {
                    const data = await imgResp.json();
                    if (data.path) {
                        document.getElementById('dalleImageContainer').innerHTML = `<h3>AI Generated Image:</h3><img src="${data.path}" alt="AI Image" style="max-width:400px;border-radius:8px;">`;
                    } else {
                        document.getElementById('dalleImageContainer').innerHTML = '<h3>AI Generated Image:</h3><p style="color:red;">Image generation failed or not available.</p>';
                    }
                } else {
                    document.getElementById('dalleImageContainer').innerHTML = '<h3>AI Generated Image:</h3><p style="color:red;">Could not fetch image path.</p>';
                }
            } finally {
                btn.disabled = false;
                btn.textContent = '🔊 Play last AI response & Generate Image';
            }
        };

        document.getElementById('demoBtn').onclick = async function(e) {
            e.preventDefault();
            // Show demo audio
            const demoAudio = document.getElementById('demoAudio');
            demoAudio.src = '/sample/sample_speech.mp3';
            demoAudio.style.display = 'block';
            demoAudio.play();
            // Show demo image
            document.getElementById('demoImageContainer').innerHTML = `<h3>Demo Image:</h3><img src="/sample/dalle_image.png" alt="Demo Image" style="max-width:400px;border-radius:8px;">`;
            // Fetch and show demo chat
            const chatResp = await fetch('/demo_chat');
            if (chatResp.ok) {
                const chatData = await chatResp.json();
                let chatHtml = "<div style='background:#e8f4fc;padding:10px;border-radius:8px;margin-top:10px;'>";
                chatData.forEach(function(msg) {
                    let role = msg.role === "user" ? "<b>You:</b>" : "<b>AI:</b>";
                    chatHtml += `<div>${role} ${msg.content}</div>`;
                });
                chatHtml += "</div>";
                document.getElementById('demoChatContainer').innerHTML = chatHtml;
            }
        };
        </script>
    '''
    return html
# New endpoint for demo chat
@app.route('/demo_chat')
def demo_chat():
    import json
    with open('sample/sample.json', 'r') as f:
        chat = json.load(f)
    return chat

def render_chat(chat_history):
    html = "<div style='background:#f4f4f4;padding:10px;border-radius:8px;'>"
    for msg in chat_history:
        role = "<b>You:</b>" if msg["role"] == "user" else "<b>AI:</b>"
        html += f"<div>{role} {msg['content']}</div>"
    html += "</div>"
    return html

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file uploaded.", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file.", 400
    text = file.read().decode('utf-8')
    session['uploaded_text'] = text
    add_to_chat("assistant", "Study guide uploaded! You can now ask questions about it.")
    return redirect(url_for('study_guide'))

@app.route('/tts', methods=['POST'])
def tts():
    chat_history = get_chat_history()
    last_ai = next((msg['content'] for msg in reversed(chat_history) if msg['role'] == 'assistant'), None)
    if not last_ai:
        return "No AI message to convert to speech.", 400
    AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT_BSMP24")
    AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY_BSMP24")
    tts_url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/tts/audio/speech?api-version=2024-02-15-preview"
    tts_headers = {
        "api-key": AZURE_OPENAI_API_KEY,
        "Content-Type": "application/json"
    }
    tts_data = {
        "model": "tts",
        "input": last_ai,
        "voice": "alloy"
    }
    tts_response = requests.post(tts_url, headers=tts_headers, data=json.dumps(tts_data))
    if tts_response.status_code == 200:
        with open('speech.mp3', 'wb') as file:
            file.write(tts_response.content)
        # Generate DALL-E image from summary prompt
        try:
            dalle_client = AzureOpenAI(api_key=os.getenv("AZURE_OPENAI_API_KEY"), azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), api_version="2024-05-01-preview")
            # Use LLM to generate a clean image prompt
            prompt_llm = f"Summarize the following for a DALL-E image prompt, avoiding any copyright or trademarked content, and make it suitable for high school students: {last_ai}"
            summary_response = openai_client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are an expert at writing safe, creative, and copyright-free prompts for DALL-E image generation for high school students."},
                    {"role": "user", "content": prompt_llm}
                ],
                max_tokens=60
            )
            image_prompt = summary_response.choices[0].message.content.strip()
            dalle_result = dalle_client.images.generate(
                model="dalle3",
                prompt=image_prompt,
                n=1
            )
            dalle_image_url = json.loads(dalle_result.model_dump_json())['data'][0]['url']
            # Download and save the image locally
            img_response = requests.get(dalle_image_url)
            img = Image.open(BytesIO(img_response.content))
            img_path = os.path.join('static', 'dalle_image.png')
            img.save(img_path)
            session['dalle_image_path'] = '/' + img_path
        except Exception as e:
            session['dalle_image_path'] = None
        return send_file('speech.mp3', mimetype='audio/mpeg')
    else:
        return f"TTS failed: {tts_response.text}", 500


# New endpoint to get the latest DALL-E image path
@app.route('/dalle_image_path')
def dalle_image_path():
    path = session.get('dalle_image_path')
    return {"path": path} if path else {"path": None}

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('study_guide'))

if __name__ == '__main__':
    app.run(debug=True)