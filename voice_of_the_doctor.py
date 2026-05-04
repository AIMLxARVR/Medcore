# fixed_voice_of_the_doctor.py with proper Bengali language support
# if you dont use pipenv uncomment the following:
# from dotenv import load_dotenv
# load_dotenv()

import os
import subprocess
import platform
import logging
from gtts import gTTS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Check if ElevenLabs API key is available
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

def text_to_speech_with_gtts(input_text, output_filepath, language="en"):
    """
    Convert text to speech using Google's Text-to-Speech service with language support
    
    Args:
        input_text (str): Text to convert to speech
        output_filepath (str): Path to save the audio file
        language (str): Language code ('en' for English, 'bn' for Bengali)
    """
    logging.info(f"Using gTTS for text-to-speech in {language} language")
    
    # Map language code to gTTS language code
    # gTTS uses 'bn' for Bengali, 'en' for English
    gtts_language = language

    try:
        audioobj = gTTS(
            text=input_text,
            lang=gtts_language,
            slow=False
        )
        audioobj.save(output_filepath)
        
        # Play the audio if possible (for debugging)
        # play_audio(output_filepath)
        
        return output_filepath
    except Exception as e:
        logging.error(f"Error in gTTS: {e}")
        return None

def text_to_speech_with_elevenlabs(input_text, output_filepath, language="en"):
    """
    Convert text to speech using ElevenLabs service if API key is available,
    otherwise fall back to gTTS. Supports multiple languages.
    
    Note: ElevenLabs may have limited Bengali support, so we'll fall back to gTTS for Bengali
    """
    # Always use gTTS for Bengali language
    if language == "bn":
        logging.info("Bengali language requested. Using gTTS for Bengali text-to-speech.")
        return text_to_speech_with_gtts(input_text, output_filepath, language)
    
    # Fall back to gTTS if ElevenLabs API key is not available
    if not ELEVENLABS_API_KEY:
        logging.warning("ElevenLabs API key not found. Falling back to gTTS.")
        return text_to_speech_with_gtts(input_text, output_filepath, language)
    
    try:
        from elevenlabs.client import ElevenLabs
        import elevenlabs
        
        logging.info("Using ElevenLabs for text-to-speech")
        client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
        audio = client.generate(
            text=input_text,
            voice="Aria",
            output_format="mp3_22050_32",
            model="eleven_turbo_v2"
        )
        elevenlabs.save(audio, output_filepath)
        
        # Play the audio if possible (for debugging)
        # play_audio(output_filepath)
        
        return output_filepath
    except ImportError:
        logging.warning("ElevenLabs library not installed. Falling back to gTTS.")
        return text_to_speech_with_gtts(input_text, output_filepath, language)
    except Exception as e:
        logging.error(f"Error in ElevenLabs: {e}")
        logging.warning("Falling back to gTTS.")
        return text_to_speech_with_gtts(input_text, output_filepath, language)

def play_audio(output_filepath):
    """
    Play audio file using appropriate command based on OS
    """
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            if output_filepath.endswith('.mp3'):
                # For Windows, we have multiple options:
                
                # Option 1: Try to use the Windows Media Player CLI
                try:
                    subprocess.run(['wmplayer', output_filepath, '/close'], shell=True)
                except Exception:
                    # Option 2: Try PowerShell Start-Process (more compatible)
                    try:
                        cmd = f'powershell -c "(New-Object Media.SoundPlayer).PlaySync();"'
                        subprocess.run(cmd, shell=True)
                    except Exception:
                        # Option 3: Just show the file without playing (last resort)
                        os.startfile(output_filepath)
            else:
                # Use SoundPlayer for WAV files
                subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
        elif os_name == "Linux":  # Linux
            # Try different players in order of preference
            players = ['mpg123', 'aplay', 'ffplay', 'mplayer']
            for player in players:
                try:
                    subprocess.run([player, output_filepath], capture_output=True)
                    break  # Stop if successful
                except FileNotFoundError:
                    continue
                except Exception as e:
                    logging.error(f"Error with {player}: {e}")
                    continue
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        logging.error(f"An error occurred while trying to play the audio: {e}")

# Function to be used in the application
def text_to_speech(input_text, output_filepath, language="en"):
    """
    Unified function that will try ElevenLabs first, then fall back to gTTS if needed.
    Supports multiple languages.
    
    Args:
        input_text (str): Text to convert to speech
        output_filepath (str): Path to save the audio file
        language (str): Language code ('en' for English, 'bn' for Bengali)
        
    Returns:
        str: Path to the audio file
    """
    try:
        # Make sure we always create MP3 files for consistency in the UI
        if not output_filepath.endswith('.mp3'):
            output_filepath = output_filepath + '.mp3'
        
        # For Bengali, always use gTTS
        if language == "bn":
            return text_to_speech_with_gtts(input_text, output_filepath, language)
            
        # For English, try ElevenLabs first then fall back
        result = text_to_speech_with_elevenlabs(input_text, output_filepath, language)
        
        # Don't try to play automatically - we'll let Gradio handle playback
        return result
    except Exception as e:
        logging.error(f"Error in text-to-speech: {e}")
        # Always ensure we have a valid output file path even if TTS fails
        try:
            # Create a simple "error" audio message in the appropriate language
            if language == "bn":
                error_message = "দুঃখিত, আমি এই প্রতিক্রিয়ার জন্য অডিও তৈরি করতে পারিনি।"
            else:
                error_message = "Sorry, I couldn't generate audio for this response."
                
            error_tts = gTTS(error_message, lang=language)
            error_tts.save(output_filepath)
        except Exception as e2:
            logging.error(f"Error creating error message audio: {e2}")
            # If even that fails, create an empty file
            with open(output_filepath, 'wb') as f:
                pass
        return output_filepath