import wave
from decouple import config
from pyaudio import PyAudio as pyaudio

import google.cloud.texttospeech as tts

def speak_file(path):
	audio_file = wave.open(path, "rb")

	audio = pyaudio()  
	stream = audio.open(
		format = audio.get_format_from_width(audio_file.getsampwidth()),  
		channels = audio_file.getnchannels(),  
		rate = audio_file.getframerate(),  
		output = True
	)

	data = audio_file.readframes(1024)  

	while data:  
		stream.write(data)  
		data = audio_file.readframes(1024)  
	
	stream.stop_stream()  
	stream.close()  

	audio.terminate()  

def generate_speech(text, path):
	text_input = tts.SynthesisInput(text=text)

	voice_params = tts.VoiceSelectionParams(
		language_code='en-GB', name="en-GB-Neural2-B"
	)
	
	audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

	client = tts.TextToSpeechClient(
		client_options={"api_key": config('GOOGLE_API_KEY'), "quota_project_id": "snidegpt"}
	)

	response = client.synthesize_speech(
		input=text_input,
		voice=voice_params,
		audio_config=audio_config,
	)

	with open(path, "wb") as audio_file:
		audio_file.write(response.audio_content)
	