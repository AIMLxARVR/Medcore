# final_updated_gradio_app.py with proper language separation
# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

# AI Doctor with Vision, Voice, and Text - now with Bengali language support
import os
import tempfile
import gradio as gr
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Import modules for different features
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
# Import the fixed voice module
from voice_of_the_doctor import text_to_speech
from enhanced_text_chat import ChatSession, process_image_query

# Initialize a chat session
chat_session = ChatSession()

# System prompts
VISION_SYSTEM_PROMPT_EN = """You are a knowledgeable medical professional providing a preliminary assessment of a patient's condition based on visual information. 

Analyze the image carefully, noting any visible symptoms or conditions. Begin your response with a compassionate acknowledgment like "Based on what I can see..." or "From my assessment..." followed by your observations.

If you identify potential medical concerns:
1. Describe what you observe in simple, clear terms
2. Offer 2-3 possible diagnoses with brief explanations 
3. Suggest appropriate home care remedies when safe to do so
4. Recommend when professional medical attention should be sought
5. Mention any relevant lifestyle factors or preventative measures

Keep your tone professional yet empathetic. Avoid medical jargon when possible, but include proper medical terminology with plain-language explanations when necessary. Balance reassurance with appropriate caution.

Structure your response in 2-3 clear paragraphs. The first should describe what you observe and potential diagnoses, and the second should focus on recommendations.

Important: Always include a disclaimer that this is not a definitive diagnosis and that the patient should consult with their healthcare provider for proper evaluation and treatment."""

# Bengali system prompt
VISION_SYSTEM_PROMPT_BN = """আপনি একজন জ্ঞানী চিকিৎসা পেশাদার যিনি ভিজ্যুয়াল তথ্যের উপর ভিত্তি করে রোগীর অবস্থার প্রাথমিক মূল্যায়ন প্রদান করছেন।

ছবিটি সাবধানে বিশ্লেষণ করুন, কোনো দৃশ্যমান লক্ষণ বা অবস্থা লক্ষ্য করুন। আপনার পর্যবেক্ষণ দিয়ে "আমি যা দেখতে পাচ্ছি তার ভিত্তিতে..." বা "আমার মূল্যায়ন থেকে..." এর মতো সহানুভূতিশীল স্বীকৃতি দিয়ে শুরু করুন।

যদি আপনি সম্ভাব্য চিকিৎসা সংক্রান্ত উদ্বেগ চিহ্নিত করেন:
1. আপনি যা পর্যবেক্ষণ করেন তা সহজ, পরিষ্কার শব্দে বর্ণনা করুন
2. সংক্ষিপ্ত ব্যাখ্যাসহ 2-3টি সম্ভাব্য রোগ নির্ণয় উল্লেখ করুন
3. যখন সম্ভব তখন উপযুক্ত ঘরোয়া যত্নের প্রতিকার সম্পর্কে পরামর্শ দিন
4. কখন পেশাদার চিকিৎসা পরামর্শ নেওয়া উচিত
5. প্রাসঙ্গিক জীবনযাপন কারণ বা প্রতিরোধমূলক ব্যবস্থা উল্লেখ করুন

আপনার সুর পেশাদার এবং সহানুভূতিশীল রাখুন। যতটা সম্ভব চিকিৎসা জার্গন এড়িয়ে চলুন, তবে প্রয়োজনে সাধারণ ভাষার ব্যাখ্যা সহ উপযুক্ত চিকিৎসা শব্দাবলী অন্তর্ভুক্ত করুন। আশ্বাস এবং উপযুক্ত সতর্কতার মধ্যে ভারসাম্য রাখুন।

আপনার প্রতিক্রিয়া 2-3টি পরিষ্কার অনুচ্ছেদে কাঠামোবদ্ধ করুন। প্রথমটি আপনি যা পর্যবেক্ষণ করেন এবং সম্ভাব্য রোগ নির্ণয়, এবং দ্বিতীয়টি সুপারিশের উপর ফোকাস করা উচিত।

গুরুত্বপূর্ণ: সর্বদা একটি দাবিত্যাগ অন্তর্ভুক্ত করুন যে এটি একটি চূড়ান্ত রোগ নির্ণয় নয় এবং রোগীর উচিত যথাযথ মূল্যায়ন এবং চিকিৎসার জন্য তাদের স্বাস্থ্যসেবা প্রদানকারীর সাথে পরামর্শ করা।"""

# Function to get system prompt based on language
def get_system_prompt(language="en"):
    """Return the appropriate system prompt based on selected language"""
    if language == "bn":
        return VISION_SYSTEM_PROMPT_BN
    else:
        return VISION_SYSTEM_PROMPT_EN

# Create a function to ensure we always have unique filenames for audio outputs
def get_unique_filename(prefix="audio", suffix=".mp3"):
    """Generate a unique filename to avoid caching issues"""
    import time
    import random
    timestamp = int(time.time())
    random_num = random.randint(1000, 9999)
    return f"{prefix}_{timestamp}_{random_num}{suffix}"

# Voice & Vision processing function
def process_voice_vision(audio_filepath, image_filepath, language="en"):
    """Process voice input and optional image"""
    # If no audio was recorded
    if not audio_filepath:
        if language == "bn":
            return "কোন অডিও রেকর্ড করা হয়নি", "অনুগ্রহ করে আপনার প্রশ্ন রেকর্ড করুন", None
        else:
            return "No audio recorded", "Please record your question", None
    
    try:
        # Transcribe the audio with the selected language
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3",
            language=language
        )
        
        # Get the appropriate system prompt based on language
        system_prompt = get_system_prompt(language)
        
        # Handle the image input if provided
        if image_filepath:
            doctor_response = analyze_image_with_query(
                query=system_prompt + speech_to_text_output, 
                encoded_image=encode_image(image_filepath),
                language=language
            )
        else:
            # If no image, just process the text query
            chat_session.add_user_message(speech_to_text_output)
            doctor_response = chat_session.get_response(language=language)
        
        # Generate voice response using unique filename
        output_filepath = get_unique_filename("voice_vision_response")
        text_to_speech(input_text=doctor_response, output_filepath=output_filepath, language=language)
        
        return speech_to_text_output, doctor_response, output_filepath
    
    except Exception as e:
        logging.error(f"Error in process_voice_vision: {e}")
        if language == "bn":
            return f"অডিও প্রক্রিয়াকরণে ত্রুটি: {str(e)}", "একটি ত্রুটি ঘটেছে। অনুগ্রহ করে আবার চেষ্টা করুন।", None
        else:
            return f"Error processing audio: {str(e)}", "An error occurred. Please try again.", None

# Function to properly handle image analysis with the updated module
def process_updated_image_query(query, image_path, language="en"):
    """Process a query with an image using the vision model"""
    if not image_path or not os.path.exists(image_path):
        if language == "bn":
            return "বিশ্লেষণের জন্য কোন বৈধ ছবি প্রদান করা হয়নি।"
        else:
            return "No valid image provided for analysis."
    
    try:
        # Get the appropriate system prompt
        system_prompt = get_system_prompt(language)
        
        encoded_image = encode_image(image_path)
        response = analyze_image_with_query(
            query=system_prompt + query, 
            encoded_image=encoded_image,
            language=language
        )
        return response
    except Exception as e:
        logging.error(f"Error in process_updated_image_query: {str(e)}")
        if language == "bn":
            return f"দুঃখিত, আমি ছবিটি বিশ্লেষণ করতে পারিনি। ত্রুটি: {str(e)}"
        else:
            return f"I'm sorry, I couldn't analyze the image. Error: {str(e)}"

# Text chat functions
def add_text(message, history):
    """Add user message to chat history"""
    # Return message immediately for display in chat
    return "", history + [[message, ""]]

def bot_response(history, image_path=None, language="en"):
    """Generate response from the assistant"""
    try:
        # Get the last user message
        user_message = history[-1][0]
        
        # Process the message with image if provided
        if image_path:
            response = process_updated_image_query(user_message, image_path, language)
            # Add the messages to chat history
            chat_session.add_user_message(user_message)
            chat_session.add_assistant_message(response)
        else:
            # Add user message to chat session and get response
            chat_session.add_user_message(user_message)
            response = chat_session.get_response(language=language)
        
        # Generate voice response with unique filename
        output_filepath = get_unique_filename(f"chat_response_{len(history)}")
        text_to_speech(input_text=response, output_filepath=output_filepath, language=language)
        
        # Update history with the response
        history[-1][1] = response
        
        return history, output_filepath
    
    except Exception as e:
        logging.error(f"Error in bot_response: {e}")
        # Update history with error message
        if language == "bn":
            error_msg = f"দুঃখিত, একটি ত্রুটি ঘটেছে: {str(e)}"
        else:
            error_msg = f"Sorry, an error occurred: {str(e)}"
            
        history[-1][1] = error_msg
        
        # Create a simple error audio message
        output_filepath = get_unique_filename("error_response")
        from gtts import gTTS
        try:
            error_tts = gTTS(error_msg, lang="bn" if language == "bn" else "en")
            error_tts.save(output_filepath)
        except:
            # If even that fails, return None
            output_filepath = None
            
        return history, output_filepath

def clear_chat():
    """Clear the chat history"""
    chat_session.clear_history()
    return None, None, None

# Create the Gradio interface
with gr.Blocks(title="AI Doctor with Vision, Voice, and Text") as app:
    # Add language selector at the top level
    with gr.Row():
        language = gr.Radio(
            ["English", "Bengali"], 
            label="Language / ভাষা", 
            value="English"
        )
    
    # English UI elements
    with gr.Group(visible=True) as en_ui:
        gr.Markdown("# AI Doctor")
        gr.Markdown("Consult with our AI Doctor using voice, image, or text")
        
        with gr.Tabs() as en_tabs:
            # Voice & Vision Tab - English
            with gr.Tab("Voice & Vision"):
                with gr.Row():
                    audio_input_en = gr.Audio(sources=["microphone"], type="filepath", label="Record your question")
                    image_input_en = gr.Image(type="filepath", label="Upload an image (if needed)")
                
                voice_submit_button_en = gr.Button("Submit")
                
                with gr.Row():
                    speech_to_text_output_en = gr.Textbox(label="What you said")
                    doctor_text_response_en = gr.Textbox(label="Doctor's Response")
                
                doctor_audio_response_en = gr.Audio(label="Doctor's Voice Response")
                
                # Voice & Vision event handler for English
                voice_submit_button_en.click(
                    fn=lambda audio, image: process_voice_vision(audio, image, "en"),
                    inputs=[audio_input_en, image_input_en],
                    outputs=[speech_to_text_output_en, doctor_text_response_en, doctor_audio_response_en]
                )
            
            # Text Chat Tab - English
            with gr.Tab("Text Chat"):
                with gr.Row():
                    with gr.Column(scale=4):
                        chatbot_en = gr.Chatbot(height=500, label="Chat with AI Doctor")
                        msg_en = gr.Textbox(
                            placeholder="Type your medical question here and press Enter",
                            label="Your message"
                        )
                        clear_en = gr.Button("Clear Conversation")
                    
                    with gr.Column(scale=1):
                        chat_image_en = gr.Image(
                            type="filepath", 
                            label="Upload an image (optional)",
                            height=300
                        )
                        audio_response_en = gr.Audio(label="Doctor's Voice Response")
                
                # Text Chat event handlers for English
                msg_en.submit(
                    add_text, 
                    [msg_en, chatbot_en], 
                    [msg_en, chatbot_en],
                    queue=False
                ).then(
                    lambda history, img: bot_response(history, img, "en"), 
                    [chatbot_en, chat_image_en], 
                    [chatbot_en, audio_response_en]
                )
                
                clear_en.click(
                    clear_chat,
                    None,
                    [chatbot_en, chat_image_en, audio_response_en]
                )
    
    # Bengali UI elements
    with gr.Group(visible=False) as bn_ui:
        gr.Markdown("# এআই ডাক্তার")
        gr.Markdown("ভয়েস, ছবি বা টেক্সট ব্যবহার করে আমাদের এআই ডাক্তারের সাথে পরামর্শ করুন")
        
        with gr.Tabs() as bn_tabs:
            # Voice & Vision Tab - Bengali
            with gr.Tab("ভয়েস এবং দৃষ্টি"):
                with gr.Row():
                    audio_input_bn = gr.Audio(sources=["microphone"], type="filepath", label="আপনার প্রশ্ন রেকর্ড করুন")
                    image_input_bn = gr.Image(type="filepath", label="একটি ছবি আপলোড করুন (যদি প্রয়োজন হয়)")
                
                voice_submit_button_bn = gr.Button("জমা দিন")
                
                with gr.Row():
                    speech_to_text_output_bn = gr.Textbox(label="আপনি যা বললেন")
                    doctor_text_response_bn = gr.Textbox(label="ডাক্তারের উত্তর")
                
                doctor_audio_response_bn = gr.Audio(label="ডাক্তারের ভয়েস প্রতিক্রিয়া")
                
                # Voice & Vision event handler for Bengali
                voice_submit_button_bn.click(
                    fn=lambda audio, image: process_voice_vision(audio, image, "bn"),
                    inputs=[audio_input_bn, image_input_bn],
                    outputs=[speech_to_text_output_bn, doctor_text_response_bn, doctor_audio_response_bn]
                )
            
            # Text Chat Tab - Bengali
            with gr.Tab("টেক্সট চ্যাট"):
                with gr.Row():
                    with gr.Column(scale=4):
                        chatbot_bn = gr.Chatbot(height=500, label="এআই ডাক্তারের সাথে চ্যাট করুন")
                        msg_bn = gr.Textbox(
                            placeholder="এখানে আপনার চিকিৎসা সংক্রান্ত প্রশ্ন টাইপ করুন এবং এন্টার চাপুন",
                            label="আপনার বার্তা"
                        )
                        clear_bn = gr.Button("কথোপকথন মুছুন")
                    
                    with gr.Column(scale=1):
                        chat_image_bn = gr.Image(
                            type="filepath", 
                            label="একটি ছবি আপলোড করুন (ঐচ্ছিক)",
                            height=300
                        )
                        audio_response_bn = gr.Audio(label="ডাক্তারের ভয়েস প্রতিক্রিয়া")
                
                # Text Chat event handlers for Bengali
                msg_bn.submit(
                    add_text, 
                    [msg_bn, chatbot_bn], 
                    [msg_bn, chatbot_bn],
                    queue=False
                ).then(
                    lambda history, img: bot_response(history, img, "bn"), 
                    [chatbot_bn, chat_image_bn], 
                    [chatbot_bn, audio_response_bn]
                )
                
                clear_bn.click(
                    clear_chat,
                    None,
                    [chatbot_bn, chat_image_bn, audio_response_bn]
                )
    
    # Language switcher
    def toggle_language(choice):
        if choice == "English":
            return gr.update(visible=True), gr.update(visible=False)
        else:
            return gr.update(visible=False), gr.update(visible=True)
    
    language.change(
        fn=toggle_language,
        inputs=[language],
        outputs=[en_ui, bn_ui]
    )

# Launch the app
app.launch(debug=True)