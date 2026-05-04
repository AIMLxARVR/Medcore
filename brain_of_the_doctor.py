# updated_brain_of_the_doctor.py with proper Bengali language support
# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

#Step1: Setup imports and logging
import os
import logging
import base64

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Step2: Setup GROQ API key
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

#Step3: Convert image to required format
def encode_image(image_path):
    """
    Convert an image file to base64 encoding
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Base64 encoded image
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        logging.error(f"Error encoding image: {e}")
        raise

#Step4: Setup Multimodal LLM 
from groq import Groq

# Updated model to use Llama 4 Scout which supports vision capabilities
DEFAULT_VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
# Fallback model if needed
FALLBACK_VISION_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"

def analyze_image_with_query(query, encoded_image, model=DEFAULT_VISION_MODEL, language="en"):
    """
    Analyze an image with a text query using a vision model with language support
    
    Args:
        query (str): The text query to accompany the image
        encoded_image (str): Base64 encoded image
        model (str): The model to use for analysis
        language (str): Language code ('en' for English, 'bn' for Bengali)
        
    Returns:
        str: The model's response
    """
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        # Add language instruction to system message based on selected language
        if language == "bn":
            system_message = """You are a medical AI assistant that speaks Bengali (Bangla) language.
Always respond in Bengali only, using Bengali script. 
Your task is to analyze the image and respond to the user's query in fluent Bengali.
Be detailed but clear in your Bengali responses."""
        else:
            system_message = """You are a medical AI assistant that speaks English.
Respond to the image analysis query in fluent English."""
        
        # Create the messages array with text and image
        messages = [
            {
                "role": "system",
                "content": system_message
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": query
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                        },
                    },
                ],
            }
        ]
        
        # Log which model we're using
        logging.info(f"Using vision model: {model} for {language} language")
        
        # Make the API request
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model,
            temperature=0.7,
            max_tokens=1024
        )

        return chat_completion.choices[0].message.content
    
    except Exception as e:
        logging.error(f"Error with primary vision model: {e}")
        
        # Try fallback model if the primary fails
        if model == DEFAULT_VISION_MODEL:
            logging.info(f"Trying fallback vision model: {FALLBACK_VISION_MODEL}")
            try:
                return analyze_image_with_query(query, encoded_image, FALLBACK_VISION_MODEL, language)
            except Exception as fallback_error:
                logging.error(f"Fallback vision model also failed: {fallback_error}")
                
        # If both models fail or we're already using the fallback
        if language == "bn":
            return f"দুঃখিত, আমি ছবিটি বিশ্লেষণ করতে পারিনি। আপনার API কী এবং ইন্টারনেট সংযোগ পরীক্ষা করুন।"
        else:
            return f"I'm sorry, I couldn't analyze the image. Please check your API key and internet connection."