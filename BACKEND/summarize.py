import os
import requests

# Hugging Face summarization model
HF_API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
HF_API_KEY = os.getenv("HF_API_KEY")  # read token from environment variable
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}  # use environment variable

def summarize_text(text):
    """
    Summarizes any text using the Hugging Face summarization model.
    Returns a summary string or an error message.
    """
    if not HF_API_KEY:
        return "Error: Hugging Face API key not set. Please set HF_API_KEY environment variable."
    
    response = requests.post(HF_API_URL, headers=HEADERS, json={"inputs": text})
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0 and "summary_text" in data[0]:
            return data[0]["summary_text"]
        else:
            return "No summary available."
    else:
        return f"Error: {response.status_code} - {response.text}"

# Quick test (run this file directly)
if __name__ == "__main__":
    test_text = "OpenAI releases GPT-5, the next generation AI language model, capable of advanced reasoning and summarization."
    print("📝 Test Summary:")
    print(summarize_text(test_text))
