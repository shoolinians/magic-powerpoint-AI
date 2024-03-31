import json
import requests

def generate_slide_json(prompt):
  """
  Generates JSON data for PowerPoint slides based on a prompt.

  Args:
      prompt: The text prompt describing the desired presentation topic.

  Returns:
      A list of dictionaries representing the JSON structure for slides.
  """

  # Replace with your desired Gemini API endpoint URL (if different)
  url = "https://YOUR_GEMINI_API_ENDPOINT/v1/models/gemini-1.0-pro:generateContent"

  # Replace with your prompt template (adjust placeholders)
  payload = {
      "prompt": f"""
      Generate JSON data for PowerPoint slides.

      Create a JSON-formatted text representing the content for a series of PowerPoint slides for the topic {prompt}. Each slide should have a title, a background image URL (replace with your image URLs), a title for the description section, a list of descriptions or bullet points, and an optional list of additional items such as images.

      The JSON structure should follow the following format:

      [
        {{
          "title": "Slide Title 1",
          "bg_image": "https://example.com/image1.jpg",  # Replace with your image URL
          "description_title": "Description Title 1",
          "description": [
            "Description/Bullet Point 1",
            "Description/Bullet Point 2",
            "Description/Bullet Point 3"
          ],
          "items": [
            {{
              "type": "image",
              "path": "https://example.com/image2.jpg"  # Replace with your image URL (optional)
            }}
          ]
        }},
        ... (more slides)
      ]

      I would like the presentation to cover the following key aspects:

      * (Key Aspect 1)
      * (Key Aspect 2)
      * (Key Aspect 3)

      **Note:** You can add or remove key aspects to customize the presentation.
      """,
      "max_tokens": 2048,
      "temperature": 0.9,
      "top_p": 1.0,
      "top_k": 1,
  }

  # Send POST request to the API
  response = requests.post(url, json=payload)

  # Check for successful response
  if response.status_code == 200:
    data = response.json()
    return data["generated_texts"][0]  # Assuming first generated text is the JSON
  else:
    print(f"Error: API request failed with status code {response.status_code}")
    return None

# Replace with your desired presentation topic
prompt = "Milkman"

# Generate JSON data
slide_data = generate_slide_json(prompt)

# Write JSON data to a file (replace with your desired filename)
if slide_data:
  with open("presentation.json", "w") as outfile:
    json.dump(slide_data, outfile, indent=4)
  print("Presentation JSON data generated successfully!")
else:
  print("Failed to generate presentation JSON data.")
