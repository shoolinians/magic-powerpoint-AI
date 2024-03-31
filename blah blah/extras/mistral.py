import requests
import re

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
    return f"Generate bullet points for a slide of a PowerPoint presentation based on the following topic: {cleaned_text}."

def main():
    raw_text = input("Enter raw text for the slide topic: ")
    prompt = generate_bullet_prompt(raw_text)
    print("Prompt:", prompt)

    # Query the model with the prompt
    model_output = query_model(prompt)
    print("Model Output:", model_output)  # Adjust as per your model's response format

if __name__ == "__main__":
    main()
