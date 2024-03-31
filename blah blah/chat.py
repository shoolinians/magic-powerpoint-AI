import torch
import requests
import re
from PIL import Image
from transformers import AutoTokenizer

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
API_TOKEN = "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"  # Replace with your actual API token
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query_model(prompt):
    payload = {"inputs": prompt}  # Adjust payload based on your model's API requirements
    print("API Request Payload:", payload)  # Print the API request payload
    response = requests.post(API_URL, headers=headers, json=payload)
    print("API Response:", response.text)  # Print the API response
    return response.json()

def clean_text(text):
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    # Remove any leading or trailing punctuation
    text = text.strip('.,!?')
    return text

def generate_bullet_prompt(raw_text):
    cleaned_text = clean_text(raw_text)
    return f'''
Generate JSON data for PowerPoint slides.

Create a JSON-formatted text representing the content for a series of PowerPoint slides for the topic {cleaned_text}. Each slide should have a title, a background image URL, a title for the description section, a list of descriptions or bullet points, and an optional list of additional items such as images.
The JSON structure should follow the following format:

[
  {{
    "title": "Slide Title 1",
    "bg_image": "Background Image URL 1",
    "description_title": "Description Title 1",
    "description": [
      "Description/Bullet Point 1",
      "Description/Bullet Point 2",
      "Description/Bullet Point 3"
    ],
    "items": [
      {{
        "type": "image",
        "path": "Image URL 1"
      }},
      {{
        "type": "image",
        "path": "Image URL 2"
      }},
      ...
    ]
  }},
  {{
    "title": "Slide Title 2",
    "bg_image": "Background Image URL 2",
    "description_title": "Description Title 2",
    "description": [
      "Description/Bullet Point 1",
      "Description/Bullet Point 2",
      ...
    ],
    "items": [
      {{
        "type": "image",
        "path": "Image URL 1"
      }},
      {{
        "type": "image",
        "path": "Image URL 2"
      }},
      ...
    ]
  }},
  ...
]

The JSON structure is generated based on the provided prompts. You can customize the titles, descriptions, and image URLs as needed for your presentation.
'''

def generate_slide_output(title, description, image_url, alt_text):
    return {
        "title": title,
        "description": description,
        "image": image_url,
        "alt": alt_text
    }

def main():
    with open('transcribed_text.txt', 'r') as file:
        raw_text = file.read()
        
    prompt = generate_bullet_prompt(raw_text)
    print("Prompt:", prompt)

    # Query the model with the prompt
    model_output = query_model(prompt)
    if isinstance(model_output, list) and len(model_output) > 0:
        # Extract relevant information from the first element of the list
        description = model_output[0]['generated_text']
        title = "Slide 1"
        image_url = "generated_image"
        alt_text = "Slide 1 Image"

        # Check if CUDA is available, then set device
        device = torch.device("cpu")

        # Generate image using Stable Diffusion model
        from diffusers import StableDiffusionPipeline
        model_id = "runwayml/stable-diffusion-v1-5"
        pipe = StableDiffusionPipeline.from_pretrained(model_id)
        pipe.model.to(device)  # Move model to device

        # Tokenize description
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
        encoded_input = tokenizer(description, return_tensors="pt")
        input_ids = encoded_input.input_ids.to(device)

        generated_image = pipe(input_ids).images[0]
        generated_image.save("generated_image.png")

        slide_output = generate_slide_output(title, description, image_url, alt_text)
        print("Slide Output:", slide_output)
    else:
        print("Error: Unexpected model output format")

if __name__ == "__main__":
    main()
