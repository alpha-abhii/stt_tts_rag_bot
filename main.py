# from flask import Flask, request
# from adding_text_to_DB import store_in_DB, delete_data_from_DB
# from RAG import RAG_bot
# app = Flask(__name__)

# import pyaudio
# import wave
# import time
# import pygame as pg
# from Speech_to_text import record_audio, convert_audio_to_mono, transcribe_audio
# from Text_to_speech import text_to_speech

# @app.route("/add_in_DB", methods=["POST", "GET"])
# def add_in_DB():
#     ## fetching the inputs
#     input = request.get_json()
#     ## getting the documents list iterating over it to store the data in vectorDB
#     documents = input['data']['documents']
#     user_ids = input['data']['user_id']
#     for doc, user_id in zip(documents, user_ids):
#         print(f"docs : {doc}, user_id : {user_id}")
#         store_in_DB(doc, user_id)
#     print("Documents are added in DB successfully!!!")

#     return {
#         "result" : "Documents are added"
#     }

# @app.route("/answer_query", methods=["POST", "GET"])
# def answer_query():
#     input = request.get_json()
#     query = input['data']['query']
#     user_id = input['data']['user_id']

#     rag_bot = RAG_bot()
#     response = rag_bot.qa_chain(query, user_id)

#     return {
#         "result" : response
#     }

# @app.route("/delete_data", methods=["POST", "GET"])
# def delete_data():
#     input = request.get_json()
#     user_id = input['data']['user_id']
#     print(user_id)

#     delete_data_from_DB(user_id)

#     return {
#         "result" : "Data deleted"
#     }

# ## the process of querying the data will begin by speech
# @app.route("/answer_speak", methods=["POST", "GET"])
# def answer_speak():
#     inp = request.get_json()
#     user_id = inp['data']['user_id']

#     record = input("Do you want to ask any question? Yes or No ---> ")

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
#         print(f"----------------------------------------------------------")
#         print(f"Text : {text}")
#         ## Now this text would go to RAG pipeline
#         rag = RAG_bot()
#         output = rag.qa_chain(text, user_id)
#         TTS_text = output["answer"]

#         ## Now this would go to TTS model
#         text_to_speech(TTS_text)
    
#         # Play the generated audio using pygame
#         print("Speaking...")
#         pg.init()
#         pg.mixer.init()
#         pg.mixer.music.load("speak.mp3")  # Load the generated MP3 file
#         pg.mixer.music.play()

#         # Wait for the audio to finish playing 
#         # A while loop is added to keep the script running until the audio finishes playing:
#         while pg.mixer.music.get_busy():
#             time.sleep(0.1)

#         print("Done playing.")
#         record = input("Do you want to ask any Question? Yes or No ---> ")
#     else:
#         print("Thank You!!!!")
#     return {
#         "result" : "Thanks"
#     }

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)





from flask import Flask, request, jsonify
from adding_text_to_DB import store_in_DB, delete_data_from_DB
from RAG import RAG_bot
import pyaudio
import wave
import time
import pygame as pg
# from Speech_to_text import record_audio, convert_audio_to_mono, transcribe_audio
from Speech_to_text import process_audio_file
from Text_to_speech import text_to_speech
import os
import base64

app = Flask(__name__)

@app.route("/add_in_DB", methods=["POST"])
def add_in_DB():
    try:
        input = request.get_json()
        documents = input['data']['documents']
        user_ids = input['data']['user_id']
        for doc, user_id in zip(documents, user_ids):
            print(f"docs : {doc}, user_id : {user_id}")
            store_in_DB(doc, user_id)
        print("Documents are added in DB successfully!!!")
        return jsonify({"result": "Documents are added"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/answer_query", methods=["POST"])
def answer_query():
    try:
        input = request.get_json()
        query = input['data']['query']
        user_id = input['data']['user_id']

        rag_bot = RAG_bot()
        response = rag_bot.qa_chain(query, user_id)

        return jsonify({"result": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/delete_data", methods=["POST"])
def delete_data():
    try:
        input = request.get_json()
        user_id = input['data']['user_id']
        print(user_id)

        delete_data_from_DB(user_id)

        return jsonify({"result": "Data deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @app.route("/answer_speak", methods=["POST"])
# def answer_speak():
#     try:
#         # Get user_id and audio file from the request
#         user_id = request.form.get("user_id")
#         audio_file = request.files.get("audio_file")

#         if not audio_file:
#             return jsonify({"error": "No audio file provided"}), 400

#         # Save the uploaded audio file
#         audio_path = "uploaded_audio.wav"
#         audio_file.save(audio_path)

#         # Convert audio to mono if needed
#         mono_audio_path = "uploaded_audio_mono.wav"
#         convert_audio_to_mono(audio_path, mono_audio_path)

#         # Transcribe audio to text
#         with wave.open(mono_audio_path, "rb") as wav_file:
#             sample_rate = wav_file.getframerate()
#         text = transcribe_audio(mono_audio_path, sample_rate)
#         print(f"Transcribed Text: {text}")

#         # Get response from RAG pipeline
#         rag = RAG_bot()
#         output = rag.qa_chain(text, user_id)
#         TTS_text = output["answer"]

#         # Convert response text to speech
#         tts_output_path = "response_audio.mp3"
#         text_to_speech(TTS_text, tts_output_path)

#         # Return the generated audio file as a response
#         with open(tts_output_path, "rb") as f:
#             audio_data = f.read()
#         audio_base64 = base64.b64encode(audio_data).decode("utf-8")

#         # Clean up temporary files
#         os.remove(audio_path)
#         os.remove(mono_audio_path)
#         os.remove(tts_output_path)

#         return jsonify({
#             "result": "Audio response generated",
#             "audio_data": audio_base64
#         }), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500



@app.route("/answer_speak", methods=["POST"])
def answer_speak():
    try:
        # Get user_id and audio file from the request
        user_id = request.form.get("user_id")
        audio_file = request.files.get("audio_file")

        if not audio_file:
            return jsonify({"error": "No audio file provided"}), 400

        # Save the uploaded audio file
        audio_path = "uploaded_audio.wav"
        audio_file.save(audio_path)

        # Process the audio file and get transcribed text
        text = process_audio_file(audio_path)

        # Get response from RAG pipeline
        rag = RAG_bot()
        output = rag.qa_chain(text, user_id)
        TTS_text = output["answer"]

        # Convert response text to speech
        tts_output_path = "response_audio.mp3"
        text_to_speech(TTS_text, tts_output_path)

        # Return the generated audio file as a response
        with open(tts_output_path, "rb") as f:
            audio_data = f.read()
        audio_base64 = base64.b64encode(audio_data).decode("utf-8")

        # Clean up temporary files
        os.remove(audio_path)
        os.remove(tts_output_path)

        return jsonify({
            "result": "Audio response generated",
            "audio_data": audio_base64
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)