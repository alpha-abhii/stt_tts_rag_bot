# import os
# import pyaudio
# import wave
# import speech_recognition as sr
# from google.cloud import speech_v1 as speech
# import pydub
# from pydub import AudioSegment
# from dotenv import load_dotenv

# CHUNK = 4096  # Increase buffer size
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 32000  # Reduce sample rate

# load_dotenv()
# # Get credentials path from environment variable
# google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# if google_credentials_path:
#     client = speech.SpeechClient.from_service_account_file(google_credentials_path)
# else:
#     raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set!")



# def record_audio(p, device_index):
#     stream = p.open(format=FORMAT,
#                         channels=CHANNELS,
#                         rate=RATE,
#                         input=True,
#                         frames_per_buffer=CHUNK,
#                         input_device_index=device_index)

#     frames = []
#     seconds = 5

#     print("Recording...")
#     for i in range(0, int(RATE / CHUNK * seconds)):
#         data = stream.read(CHUNK, exception_on_overflow=False)
#         frames.append(data)

#     print("Recording Stopped")

#     stream.stop_stream()
#     stream.close()
#     p.terminate()

#     ## saving the recording
#     wf = wave.open("output.wav", 'wb')
#     wf.setnchannels(CHANNELS)
#     wf.setsampwidth(p.get_sample_size(FORMAT))
#     wf.setframerate(RATE)
#     wf.writeframes(b''.join(frames))
#     wf.close()

# def convert_audio_to_mono(input_file, output_file):
#     audio = AudioSegment.from_file(input_file)
#     audio = audio.set_channels(1)
#     audio.export(output_file, format="wav")
#     print("Convered to mono")

# def transcribe_audio(input_file, sample_rate):

#     with open(input_file, 'rb') as audio_file:
#         content = audio_file.read()
#         audio = speech.RecognitionAudio(content=content)
#         config = speech.RecognitionConfig(
#             encoding= speech.RecognitionConfig.AudioEncoding.LINEAR16,
#             sample_rate_hertz = sample_rate,
#             language_code='en-US',

#         )

#         response = client.recognize(config=config, audio=audio)
#         for result in response.results:
#             return result.alternatives[0].transcript
#             ## print(f"Transcript : {result.alternatives[0].transcript}")
#             ## print(f"Confidence : {result.alternatives[0].confidence}")
        
#     return response

# if __name__ == "__main__":

#     record = input("Do you want to speak? Yes or No ---> ")
#     while record == "Yes":

#         p = pyaudio.PyAudio()

#         # Find the correct input device index
#         device_index = None
#         for i in range(p.get_device_count()):
#             device_info = p.get_device_info_by_index(i)
#             if "Microphone" in device_info["name"]:  # Adjust based on your mic name
#                 device_index = i
#                 break

#         record_audio(p, device_index)

#         with wave.open("output.wav", "rb") as wav_file:
#             sample_rate = wav_file.getframerate()
#             print(f"Sample rate : {sample_rate}")

#         convert_audio_to_mono("output.wav", "output_mono.wav")
#         text = transcribe_audio("output_mono.wav", sample_rate)
#         print(f"Text : {text}")

#         record = input("Do you want to speak? Yes or No ---> ")
#     else:
#         print("Thank You!!!!")



import os
import wave
from google.cloud import speech_v1 as speech
from pydub import AudioSegment
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get credentials path from environment variable
google_credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if google_credentials_path:
    client = speech.SpeechClient.from_service_account_file(google_credentials_path)
else:
    raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set!")

def convert_audio_to_mono(input_file, output_file):
    """
    Converts an audio file to mono and saves it to the specified output file.

    Args:
        input_file (str): Path to the input audio file.
        output_file (str): Path to save the mono audio file.
    """
    try:
        audio = AudioSegment.from_file(input_file)
        audio = audio.set_channels(1)
        audio.export(output_file, format="wav")
        print(f"Converted {input_file} to mono and saved to {output_file}")
    except Exception as e:
        print(f"Error in convert_audio_to_mono: {e}")
        raise

def transcribe_audio(input_file, sample_rate):
    """
    Transcribes the given audio file using Google Speech-to-Text API.

    Args:
        input_file (str): Path to the audio file.
        sample_rate (int): Sample rate of the audio file.

    Returns:
        str: The transcribed text.
    """
    try:
        with open(input_file, "rb") as audio_file:
            content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=sample_rate,
                language_code="en-US",
            )

            response = client.recognize(config=config, audio=audio)
            if response.results:
                return response.results[0].alternatives[0].transcript
            else:
                return None
    except Exception as e:
        print(f"Error in transcribe_audio: {e}")
        raise

def process_audio_file(audio_file_path):
    """
    Processes an audio file: converts it to mono and transcribes it.

    Args:
        audio_file_path (str): Path to the audio file.

    Returns:
        str: The transcribed text.
    """
    try:
        # Convert audio to mono
        mono_audio_path = "temp_mono.wav"
        convert_audio_to_mono(audio_file_path, mono_audio_path)

        # Get sample rate
        with wave.open(mono_audio_path, "rb") as wav_file:
            sample_rate = wav_file.getframerate()

        # Transcribe audio
        text = transcribe_audio(mono_audio_path, sample_rate)

        # Clean up temporary mono file
        os.remove(mono_audio_path)

        return text
    except Exception as e:
        print(f"Error in process_audio_file: {e}")
        raise

if __name__ == "__main__":
    # Example usage for local testing
    audio_file = "output.wav"  # Replace with your audio file path
    if os.path.exists(audio_file):
        transcribed_text = process_audio_file(audio_file)
        print(f"Transcribed Text: {transcribed_text}")
    else:
        print(f"Audio file {audio_file} not found.")