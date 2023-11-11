import os, wave, struct, tempfile, pyaudio

from google.cloud import speech
import google.cloud.texttospeech as tts
from openai import OpenAI as ai

import pvporcupine, pvrecorder, pvcobra

cobra = pvcobra.create(access_key=os.environ['PICOVOICE_KEY'])
client = speech.SpeechClient()

porcupine = pvporcupine.create(
  access_key=os.environ['PICOVOICE_KEY'],
  keyword_paths=['./yobro.ppn'],
  sensitivities=[1]
)

recorder = pvrecorder.PvRecorder(frame_length=512, device_index=0)

try:
	while True:
		print('----------')
		recorder.start()

		frame = recorder.read()
		keyword_index = -1

		while keyword_index == -1:
			frame = recorder.read()
			keyword_index = porcupine.process(frame)

		voice_probability = cobra.process(frame)
		command = []

		print('detected')

		while voice_probability < 0.8:
			frame = recorder.read()
			command.extend(frame)
			voice_probability = cobra.process(frame)

		print('start comand')

		while voice_probability > 0.2:
			frame = recorder.read()
			command.extend(frame)
			voice_probability = cobra.process(frame)

		print('end command')

		recorder.stop()

		print('saving file')

		with wave.open('./test.wav', 'w') as f:
			f.setparams((1, 2, 16000, 512, "NONE", "NONE"))
			f.writeframes(struct.pack("h" * len(command), *command))

		with open('./test.wav', "rb") as audio_file:
			content = audio_file.read()

		# In practice, stream should be a generator yielding chunks of audio data.
		stream = [content]

		requests = (
			speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream
		)

		config = speech.RecognitionConfig(
			encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
			sample_rate_hertz=16000,
			language_code="en-GB",
		)

		streaming_config = speech.StreamingRecognitionConfig(config=config)

		# streaming_recognize returns a generator.
		responses = client.streaming_recognize(
			config=streaming_config,
			requests=requests,
		)

		for response in responses:
			# Once the transcription has settled, the first result will contain the
			# is_final result. The other results will be for subsequent portions of
			# the audio.
			for result in response.results:
				alternatives = result.alternatives
				# The alternatives are ordered from most likely to least.
				for alternative in alternatives:
					completion = ai().chat.completions.create(
						model = "gpt-3.5-turbo",
						messages = [
							{"role": "system", "content": "You are a sarcastic assistant that answers questions reluctantly and in no more than one sentence, as well as subtly insulting the user, and never prompting for more input"},
							{"role": "user", "content": alternative.transcript}
						]
					)
			
			print(completion.choices[0].message.content)
	
			text_input = tts.SynthesisInput(text=completion.choices[0].message.content)
			voice_params = tts.VoiceSelectionParams(
				language_code='en-GB', name="en-GB-Neural2-B"
			)
			audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

			client = tts.TextToSpeechClient()
			response = client.synthesize_speech(
				input=text_input,
				voice=voice_params,
				audio_config=audio_config,
			)

			with open("./output.wav", "wb") as out:
				out.write(response.audio_content)
				print('Generated speech saved')

			f = wave.open("./output.wav","rb")
			p = pyaudio.PyAudio()  
			stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True)
			data = f.readframes(1024)  
			#play stream  
			while data:  
				stream.write(data)  
				data = f.readframes(1024)  
			
			#stop stream  
			stream.stop_stream()  
			stream.close()  
			
			#close PyAudio  
			p.terminate()  

except KeyboardInterrupt:
    pass

recorder.stop()
recorder.delete()