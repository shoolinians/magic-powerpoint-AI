import requests
import re
import torch
from PIL import Image
from torchvision import transforms
from io import BytesIO
from diffusers import StableDiffusionPipeline

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
API_TOKEN = "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"  # Replace with your actual API token
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query_model(prompt):
    payload = {"inputs": prompt} 
    print("API Request Payload:", payload)
    response = requests.post(API_URL, headers=headers, json=payload)
    print("API Response:", response.text) 
    return response.json()

def clean_text(text):
    # Remove extra whitespaces
    text = re.sub(r'\s+', ' ', text)
    # Remove any leading or trailing punctuation
    text = text.strip('.,!?')
    return text

def generate_bullet_prompt(raw_text):
    cleaned_text = clean_text(raw_text)
    return f"""Generate bullet points for a slide of a PowerPoint presentation based on the following topic: {cleaned_text}."""

def generate_slide_output(title, description, image_url, alt_text):
    return {
        "title": title,
        "description": description,
        "image": image_url,
        "alt": alt_text
    }

def generate_image_with_pytorch(description):
    # Load the Stable Diffusion model
    model_id = "CompVis/stable-diffusion-v1-4"  
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")  # Assuming you have a CUDA-enabled GPU
    print(f"Loaded Model: {pipe}")  # Print the loaded model info

    image = pipe(description, num_inference_steps=20).images[0]  # Add guidance
    image.save("generated_image.png") 
    return image



def main():
    raw_text = input("Enter raw text for the slide topic: ")
    prompt = generate_bullet_prompt(raw_text)
    print("Prompt:", prompt)

    # Query the model with the prompt
    model_output = query_model(prompt)
    if isinstance(model_output, list) and len(model_output) > 0:
        description = model_output[0]['generated_text']
        title = "Slide 1" 
        alt_text = "Slide 1 Image"

        # Generate the image
        generated_image = generate_image_with_pytorch(description) 

        # Create the slide output 
        slide_output = generate_slide_output(title, description, "generated_image.png", alt_text)
        print("Slide Output:", slide_output)
    else:
        print("Error: Unexpected model output format")

if __name__ == "__main__":
    main()
