# enhanced_text_chat.py - Streamlit optimized version with Bengali language support
# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

import os
import logging
import streamlit as st
from groq import Groq
from brain_of_the_doctor import encode_image, analyze_image_with_query

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Groq API
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
DEFAULT_MODEL = "meta-llama/llama-4-maverick-17b-128e-instruct"

# System prompts for different languages
ENGLISH_SYSTEM_PROMPT = """You are a knowledgeable and compassionate medical AI assistant. 
Your role is to provide preliminary medical information and guidance in response to user inquiries.

When responding to medical questions:
1. Offer clear, accurate information based on established medical knowledge
2. Explain potential conditions or symptoms in accessible language
3. Suggest appropriate home care when safe and applicable
4. Recommend when professional medical attention should be sought
5. Always emphasize that you're providing general information, not a diagnosis

Balance reassurance with appropriate caution. Avoid technical jargon when possible, but include medical terminology with plain-language explanations when necessary.

Important: Always include a disclaimer clarifying that your information is not a substitute for professional medical advice, diagnosis, or treatment."""

BENGALI_SYSTEM_PROMPT = """আপনি একজন জ্ঞানী ও সহানুভূতিশীল মেডিকেল এআই সহকারী।
আপনার ভূমিকা হল ব্যবহারকারীর প্রশ্নের উত্তরে প্রাথমিক চিকিৎসা তথ্য ও নির্দেশনা প্রদান করা।

চিকিৎসা সংক্রান্ত প্রশ্নের উত্তর দেওয়ার সময়:
1. প্রতিষ্ঠিত চিকিৎসা জ্ঞানের উপর ভিত্তি করে স্পষ্ট, সঠিক তথ্য দিন
2. সম্ভাব্য অবস্থা বা লক্ষণগুলি সহজ ভাষায় ব্যাখ্যা করুন
3. যখন নিরাপদ এবং প্রযোজ্য তখন উপযুক্ত ঘরোয়া যত্নের পরামর্শ দিন
4. কখন পেশাদার চিকিৎসা মনোযোগ নেওয়া উচিত তা সুপারিশ করুন
5. সর্বদা জোর দিন যে আপনি সাধারণ তথ্য প্রদান করছেন, রোগ নির্ণয় নয়

উপযুক্ত সতর্কতার সাথে আশ্বাস ভারসাম্য করুন। যখন সম্ভব টেকনিক্যাল জার্গন এড়িয়ে চলুন, তবে প্রয়োজনে সাধারণ-ভাষার ব্যাখ্যাসহ চিকিৎসা শব্দাবলী অন্তর্ভুক্ত করুন।

গুরুত্বপূর্ণ: সর্বদা একটি দাবিত্যাগ অন্তর্ভুক্ত করুন যে আপনার তথ্য পেশাদার চিকিৎসা পরামর্শ, রোগ নির্ণয় বা চিকিৎসার বিকল্প নয়।"""

# Function to get the appropriate system prompt based on language
def get_system_prompt(language="en"):
    """Return the system prompt for the specified language"""
    if language == "bn":
        return BENGALI_SYSTEM_PROMPT
    else:
        return ENGLISH_SYSTEM_PROMPT


class ChatSession:
    """Manage a conversation between the user and the AI doctor - Streamlit optimized"""
    
    def __init__(self):
        self.history = []
        self.client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
        
        if not self.client:
            if 'api_key_warning_shown' not in st.session_state:
                st.error("GROQ API key not found. Please set your GROQ_API_KEY environment variable.")
                st.session_state.api_key_warning_shown = True
        
    def add_user_message(self, message):
        """Add a user message to the chat history"""
        self.history.append({"role": "user", "content": message})
        
    def add_assistant_message(self, message):
        """Add an assistant message to the chat history"""
        self.history.append({"role": "assistant", "content": message})
        
    def get_response(self, language="en"):
        """Generate a response from the AI doctor based on the chat history"""
        if not self.client:
            if language == "bn":
                return "দুঃখিত, API কী পাওয়া যায়নি। অনুগ্রহ করে আপনার GROQ_API_KEY সেট করুন।"
            else:
                return "Sorry, API key not found. Please set your GROQ_API_KEY."
        
        try:
            # Get the appropriate system prompt based on language
            system_prompt = get_system_prompt(language)
            
            # Create the messages array with the system prompt
            messages = [{"role": "system", "content": system_prompt}]
            
            # Add the chat history
            messages.extend(self.history)
            
            # Generate the response
            logging.info("Generating response from model...")
            
            # Use Streamlit's progress and status for better UX
            with st.status("Generating response...", expanded=False) as status:
                response = self.client.chat.completions.create(
                    messages=messages,
                    model=DEFAULT_MODEL,
                    temperature=0.7,
                    max_tokens=1024,
                    stream=False
                )
                status.update(label="Response generated!", state="complete")
            
            # Extract the response text
            assistant_message = response.choices[0].message.content
            
            # Add the assistant's response to the chat history
            self.add_assistant_message(assistant_message)
            
            return assistant_message
            
        except Exception as e:
            logging.error(f"Error generating response: {e}")
            
            # Return error message in the appropriate language
            if language == "bn":
                error_msg = f"দুঃখিত, একটি ত্রুটি ঘটেছে: {str(e)}"
            else:
                error_msg = f"Sorry, an error occurred: {str(e)}"
                
            # Show error in Streamlit
            st.error(error_msg)
            return error_msg
            
    def clear_history(self):
        """Clear the chat history"""
        self.history = []
        logging.info("Chat history cleared")

    def get_history_length(self):
        """Get the number of messages in chat history"""
        return len(self.history)

    def get_last_user_message(self):
        """Get the last user message"""
        user_messages = [msg for msg in self.history if msg["role"] == "user"]
        return user_messages[-1]["content"] if user_messages else None

    def get_last_assistant_message(self):
        """Get the last assistant message"""
        assistant_messages = [msg for msg in self.history if msg["role"] == "assistant"]
        return assistant_messages[-1]["content"] if assistant_messages else None


@st.cache_data
def process_image_query(query, image_path, language="en"):
    """Process a query with an image - cached for better performance"""
    try:
        # Get the appropriate system prompt
        system_prompt = get_system_prompt(language)
        
        # Encode the image
        encoded_image = encode_image(image_path)
        
        # Analyze the image with the query
        with st.status("Analyzing image...", expanded=False) as status:
            response = analyze_image_with_query(
                query=f"{system_prompt}\n\n{query}", 
                encoded_image=encoded_image,
                language=language
            )
            status.update(label="Image analysis complete!", state="complete")
        
        return response
        
    except Exception as e:
        logging.error(f"Error processing image query: {e}")
        
        # Return error message in the appropriate language
        if language == "bn":
            error_msg = f"দুঃখিত, ছবি বিশ্লেষণ করতে একটি ত্রুটি ঘটেছে: {str(e)}"
        else:
            error_msg = f"Sorry, an error occurred while analyzing the image: {str(e)}"
            
        st.error(error_msg)
        return error_msg


def display_chat_message(message, is_user=True, audio_file=None):
    """Display a chat message with proper styling"""
    if is_user:
        with st.chat_message("user"):
            st.write(message)
    else:
        with st.chat_message("assistant"):
            st.write(message)
            if audio_file and os.path.exists(audio_file):
                st.audio(audio_file, format="audio/mp3")


def format_medical_response(response, language="en"):
    """Format medical response with proper structure and warnings"""
    if language == "bn":
        disclaimer = "\n\n⚠️ **গুরুত্বপূর্ণ দাবিত্যাগ**: এই তথ্য শুধুমাত্র সাধারণ নির্দেশনার জন্য। চূড়ান্ত রোগ নির্ণয় এবং চিকিৎসার জন্য একজন যোগ্য চিকিৎসকের সাথে পরামর্শ করুন।"
    else:
        disclaimer = "\n\n⚠️ **Important Disclaimer**: This information is for general guidance only. Please consult with a qualified healthcare provider for proper diagnosis and treatment."
    
    # Add disclaimer if not already present
    if "disclaimer" not in response.lower() and "দাবিত্যাগ" not in response.lower():
        response += disclaimer
    
    return response


# Streamlit-specific utility functions
def initialize_chat_session():
    """Initialize chat session in Streamlit session state"""
    if 'chat_session' not in st.session_state:
        st.session_state.chat_session = ChatSession()
    return st.session_state.chat_session


def reset_chat_session():
    """Reset the chat session"""
    if 'chat_session' in st.session_state:
        st.session_state.chat_session.clear_history()
    
    # Clear chat history from session state as well
    if 'chat_history_en' in st.session_state:
        st.session_state.chat_history_en = []
    if 'chat_history_bn' in st.session_state:
        st.session_state.chat_history_bn = []


def get_chat_stats(language="en"):
    """Get chat statistics for display"""
    if 'chat_session' not in st.session_state:
        return {"total_messages": 0, "user_messages": 0, "assistant_messages": 0}
    
    history = st.session_state.chat_session.history
    user_messages = len([msg for msg in history if msg["role"] == "user"])
    assistant_messages = len([msg for msg in history if msg["role"] == "assistant"])
    
    return {
        "total_messages": len(history),
        "user_messages": user_messages,
        "assistant_messages": assistant_messages
    }