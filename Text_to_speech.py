# from google.cloud import texttospeech
# import os
# import time
# import pygame as pg
# from dotenv import load_dotenv

# load_dotenv()

# # Get credentials path from environment variable
# google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# if google_credentials_path:
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials_path
# else:
#     raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set!")

# def text_to_speech(text):

#     ## initialize the client
#     client = texttospeech.TextToSpeechClient()
#     # Set the text input to be synthesized
#     synthesis_input = texttospeech.SynthesisInput(text=text)

#     # Build the voice request
#     voice = texttospeech.VoiceSelectionParams(
#         language_code="en-US",  # Language code (e.g., "en-US" or "en-GB")
#         name="en-US-Wavenet-D",  # Voice name (e.g., "en-US-Wavenet-D")
#         ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL  # Gender (NEUTRAL, MALE, FEMALE)
#     )

#     # Select the type of audio file
#     audio_config = texttospeech.AudioConfig(
#         audio_encoding=texttospeech.AudioEncoding.MP3  # Output format (MP3, LINEAR16, etc.)
#     )

#     # Perform the text-to-speech request
#     response = client.synthesize_speech(
#         input=synthesis_input, voice=voice, audio_config=audio_config
#     )

#     output_file = "speak.mp3"
#     # Save the audio to a file
#     with open(output_file, "wb") as out:
#         out.write(response.audio_content)
#         print(f"Audio content written to '{output_file}'")

# if __name__ == "__main__":

#     text = "Hii, My name is Umesh Kumar!!!!"
#     text_to_speech(text)
    
#     # Play the generated audio using pygame
#     print("Speaking...")
#     pg.init()
#     pg.mixer.init()
#     pg.mixer.music.load("speak.mp3")  # Load the generated MP3 file
#     pg.mixer.music.play()

#     # Wait for the audio to finish playing 
#     # A while loop is added to keep the script running until the audio finishes playing:
#     while pg.mixer.music.get_busy():
#         time.sleep(0.1)

#     print("Done playing.")





from google.cloud import texttospeech
import os
from dotenv import load_dotenv

load_dotenv()

# Get credentials path from environment variable
google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if google_credentials_path:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_credentials_path
else:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set!")

def text_to_speech(text, output_path):
    """
    Converts the given text to speech and saves it to the specified output path.

    Args:
        text (str): The text to convert to speech.
        output_path (str): The path where the generated audio file will be saved.
    """
    try:
        # Initialize the client
        client = texttospeech.TextToSpeechClient()

        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",  # Language code (e.g., "en-US" or "en-GB")
            name="en-US-Wavenet-D",  # Voice name (e.g., "en-US-Wavenet-D")
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL  # Gender (NEUTRAL, MALE, FEMALE)
        )

        # Select the type of audio file
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3  # Output format (MP3, LINEAR16, etc.)
        )

        # Perform the text-to-speech request
        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        # Save the audio to the specified output path
        with open(output_path, "wb") as out:
            out.write(response.audio_content)
            print(f"Audio content written to '{output_path}'")

    except Exception as e:
        print(f"Error in text_to_speech: {e}")
        raise

if __name__ == "__main__":
    # Example usage
    text = "Hi, My name is Umesh Kumar!"
    output_file = "speak.mp3"
    text_to_speech(text, output_file)