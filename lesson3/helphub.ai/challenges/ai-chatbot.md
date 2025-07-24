
## AI-Chatbot Feature Integration

### Objective
Integrate Azure OpenAI services into your Flask application using GitHub Copilot assistance.

### Prerequisites
- Basic Flask website structure already created
- Azure OpenAI resource deployed in Azure portal
- Azure OpenAI API key and endpoint URL

### Step-by-Step Instructions

**Step 1: Choose Your Azure OpenAI Feature (5 minutes)**
- Decide on one Azure OpenAI feature to implement:
  - **Chatbot** using GPT-4 or GPT-3.5-turbo
  - **Text completion** for content generation
  - **Code assistant** for programming help
  - **Creative writing** tool for content creation

**Step 2: Set Up Azure OpenAI Integration (8 minutes)**
1. Create a `.env` file for Azure OpenAI credentials:
   ```
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2024-02-01
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1
   ```

2. Create a `requirements.txt` file with dependencies:
   ```
   Flask==2.3.3
  openai>=1.6.0
  python-dotenv==1.0.0
   ```

3. Install Python packages: `pip install -r requirements.txt`

4. Use Copilot prompt: `# Create Python function to load Azure OpenAI environment variables`

5. Use Copilot to generate Azure OpenAI client setup:
   ```python
   # Import openai and create AzureOpenAI client with environment variables
   ```

6. Test the connection with Copilot: `# Test Azure OpenAI connection and print available models`

**Step 3: Build the Frontend Interface **
1. Prompt Copilot: `<!-- Create a Flask template with chat interface using Jinja2 for Azure OpenAI chatbot -->`
2. Add CSS styling with Copilot: `/* Style a modern chat interface with bubbles for AI conversation */`
3. Create Flask template with form handling:
   ```python
   # Create Flask route to render chat template and handle form submissions
   ```
4. Use Copilot for template structure: `<!-- Create HTML form that submits to Flask route for chat messages -->`

**Step 4: Connect Flask Backend with Azure OpenAI **
1. Use Copilot to create Flask route: `# Flask route to handle chat messages and call Azure OpenAI API`
2. Implement Azure OpenAI API call with proper error handling:
   ```python
   # Create Flask route that sends user message to Azure OpenAI and returns JSON response
   ```
3. Use Copilot for client configuration: `# Configure openai client for Azure with api_key, azure_endpoint, and api_version`
4. Add response handling: `# Handle Azure OpenAI chat completion response and extract message content`
5. Implement error handling for Azure OpenAI API errors and rate limits

**Step 5: Test and Debug Azure OpenAI Integration **
1. Test with various prompts to Azure OpenAI
2. Use Copilot to fix any errors: `# Debug Azure OpenAI API connection and authentication issues`
3. Verify deployment name and endpoint configuration
4. Test edge cases like empty messages and API timeouts

### Example Python Code Structure:
```python
# Use this as reference - ask Copilot to generate similar code
import os
from openai import AzureOpenAI
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables and create Azure OpenAI client
# Create Flask route for /chat that accepts POST requests
# Handle user messages and return AI responses as JSON
```
