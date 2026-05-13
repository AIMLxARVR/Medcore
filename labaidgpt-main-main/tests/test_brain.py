import pytest
from unittest.mock import patch, mock_open
import base64
import os
from src.brain import brain_of_the_doctor

# Test for encode_image function
def test_encode_image():
    # Create a dummy image file
    dummy_image_content = b"dummy image data"
    dummy_image_path = "dummy_image.jpg"
    with open(dummy_image_path, "wb") as f:
        f.write(dummy_image_content)

    # Call the function
    encoded_string = brain_of_the_doctor.encode_image(dummy_image_path)

    # Clean up the dummy file
    os.remove(dummy_image_path)

    # Check if the output is a base64 encoded string
    assert isinstance(encoded_string, str)
    # Decode and check if the content matches
    decoded_bytes = base64.b64decode(encoded_string)
    assert decoded_bytes == dummy_image_content

def test_encode_image_file_not_found():
    with pytest.raises(FileNotFoundError):
        brain_of_the_doctor.encode_image("non_existent_file.jpg")

# Test for analyze_image_with_query function using mock
def test_analyze_image_with_query(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test_api_key")
    with patch('src.brain.brain_of_the_doctor.Groq') as mock_groq:
        # Mock the API response
        mock_response = "This is a test analysis."
        mock_groq.return_value.chat.completions.create.return_value.choices = [
            type('Choice', (), {'message': type('Message', (), {'content': mock_response})})()
        ]

        # Dummy data
        query = "Analyze this image"
        encoded_image = "dummy_encoded_image_string"
        language = "en"

        # Call the function
        result = brain_of_the_doctor.analyze_image_with_query(query, encoded_image, language=language)

        # Assert that the mocked API was called
        mock_groq.return_value.chat.completions.create.assert_called_once()
        # Assert that the result is what we expect from the mock
        assert result == mock_response

def test_analyze_image_with_query_api_error(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test_api_key")
    with patch('src.brain.brain_of_the_doctor.Groq') as mock_groq:
        # Simulate an API error
        mock_groq.return_value.chat.completions.create.side_effect = Exception("API connection failed")

        query = "Analyze this"
        encoded_image = "dummy_string"
        language = "en"

        # The function should catch the exception and return an error message
        result = brain_of_the_doctor.analyze_image_with_query(query, encoded_image, language=language)
        assert "I'm sorry, I couldn't analyze the image." in result
