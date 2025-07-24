from openai import AzureOpenAI
import os
import json
import dotenv
# Load environment variables
dotenv.load_dotenv()

# Get the keys and variables from environment
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
client2 = AzureOpenAI(api_key=AZURE_OPENAI_API_KEY, azure_endpoint=AZURE_OPENAI_ENDPOINT, api_version="2024-05-01-preview")

result = client2.images.generate(
    model="dalle3", # the name of your DALL-E 3 deployment
    prompt="pacmanplaying chess",
    n=1
)

image_url = json.loads(result.model_dump_json())['data'][0]['url']

print(image_url)
#save the image
import requests
from PIL import Image
from io import BytesIO

response = requests.get(image_url)
img = Image.open(BytesIO(response.content))
img.save("dalle_image2.png")