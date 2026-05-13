import pytest
from unittest.mock import patch
import os
import importlib
from src.voice import voice_of_the_doctor

# Fixture to set environment variables and reload the module
@pytest.fixture
def mock_elevenlabs(monkeypatch):
    """Fixture to mock ElevenLabs and set API key."""
    monkeypatch.setenv("ELEVENLABS_API_KEY", "test_api_key")
    # We need to ensure elevenlabs can be imported by the function under test
    # The actual library will be replaced by the mock.
    try:
        import elevenlabs
    except ImportError:
        # If elevenlabs is not installed, we can mock it at the sys.modules level.
        # However, it should be in requirements.txt.
        pass
    importlib.reload(voice_of_the_doctor)

# Test gTTS fallback when ElevenLabs key is not present
def test_text_to_speech_gtts_fallback(monkeypatch):
    monkeypatch.delenv("ELEVENLABS_API_KEY", raising=False)
    importlib.reload(voice_of_the_doctor)

    with patch('src.voice.voice_of_the_doctor.gTTS') as mock_gtts:
        instance = mock_gtts.return_value
        input_text = "Hello from gTTS"
        output_filepath = "test_gtts.mp3"

        result_path = voice_of_the_doctor.text_to_speech(input_text, output_filepath, language="en")

        mock_gtts.assert_called_once_with(text=input_text, lang="en", slow=False)
        instance.save.assert_called_once_with(output_filepath)
        assert result_path == output_filepath

# Test ElevenLabs integration
def test_text_to_speech_with_elevenlabs(mock_elevenlabs):
    with patch('elevenlabs.client.ElevenLabs') as mock_elevenlabs_client, \
         patch('elevenlabs.save') as mock_elevenlabs_saver:

        client_instance = mock_elevenlabs_client.return_value
        mock_audio_data = b"mock audio data"
        client_instance.generate.return_value = mock_audio_data

        input_text = "Hello from ElevenLabs"
        output_filepath = "test_elevenlabs.mp3"

        result_path = voice_of_the_doctor.text_to_speech(input_text, output_filepath, language="en")

        mock_elevenlabs_client.assert_called_once_with(api_key="test_api_key")
        client_instance.generate.assert_called_once()
        mock_elevenlabs_saver.assert_called_once_with(mock_audio_data, output_filepath)
        assert result_path == output_filepath

# Test Bengali language always uses gTTS
def test_bengali_language_uses_gtts(mock_elevenlabs):
    with patch('src.voice.voice_of_the_doctor.gTTS') as mock_gtts:
        instance = mock_gtts.return_value
        input_text = "বাংলা পরীক্ষা"
        output_filepath = "test_bengali.mp3"

        result_path = voice_of_the_doctor.text_to_speech(input_text, output_filepath, language="bn")

        mock_gtts.assert_called_once_with(text=input_text, lang="bn", slow=False)
        instance.save.assert_called_once_with(output_filepath)
        assert result_path == output_filepath

# Test error handling in ElevenLabs falls back to gTTS
def test_elevenlabs_error_fallback(mock_elevenlabs):
    # We patch the lookup of the ElevenLabs client, which happens inside the function
    with patch('elevenlabs.client.ElevenLabs', side_effect=Exception("API Error")), \
         patch('src.voice.voice_of_the_doctor.gTTS') as mock_gtts:

        instance = mock_gtts.return_value
        input_text = "Fallback test"
        output_filepath = "test_fallback.mp3"

        result_path = voice_of_the_doctor.text_to_speech(input_text, output_filepath, language="en")

        mock_gtts.assert_called_with(text=input_text, lang="en", slow=False)
        instance.save.assert_called_once_with(output_filepath)
        assert result_path == output_filepath
