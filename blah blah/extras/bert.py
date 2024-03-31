import requests
import re
import torch
from PIL import Image
from torchvision import transforms
from io import BytesIO
from diffusers import StableDiffusionPipeline
import json
import os

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

def generate_slide_prompt(raw_text):
    cleaned_text = clean_text(raw_text)
    return f"Generate slide image for a slide of a PowerPoint presentation based on the following topic: {cleaned_text}."

def generate_slide_image(description):
    # Load the Stable Diffusion model
    model_id = "CompVis/stable-diffusion-v1-4"  
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")  # Assuming you have a CUDA-enabled GPU
    print(f"Loaded Model: {pipe}")  # Print the loaded model info

    image = pipe(description, num_inference_steps=20).images[0]  # Add guidance
    return image


def main():
    # Create a folder to store images if it doesn't exist
    image_folder = "images"
    if not os.path.exists(image_folder):
        os.makedirs(image_folder)

    num_slides = int(input("Enter the number of slides: "))
    raw_text_list = [input(f"Enter raw text for slide {i + 1}: ") for i in range(num_slides)]

    presentation_data = []

    for i, raw_text in enumerate(raw_text_list):
        prompt = generate_slide_prompt(raw_text)
        print("Prompt:", prompt)

        # Query the model with the prompt
        model_output = query_model(prompt)
        if isinstance(model_output, list) and len(model_output) > 0:
            description = model_output[0]['generated_text']
            title = f"Slide {i + 1}"
            image_name = f"slide_{i+1}.jpg"
            image_path = os.path.join(image_folder, image_name)

            # Generate and save the slide image
            slide_image = generate_slide_image(description)
            slide_image.save(image_path)

            # Create the slide data
            slide_data = {
                "title": title,
                "image": image_path
            }
            presentation_data.append(slide_data)
        else:
            print("Error: Unexpected model output format")

    # Write the presentation data to a JSON file
    with open("presentation_data.json", "w") as json_file:
        json.dump(presentation_data, json_file, indent=2)

    print("Presentation data written to presentation_data.json")

if __name__ == "__main__":
    main()
