from decouple import config
from google.cloud import speech

client = speech.SpeechClient(
	client_options={"api_key": config('GOOGLE_API_KEY'), "quota_project_id": "snidegpt"}
)

def transcribe_file(path):
	config = speech.RecognitionConfig(encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16, sample_rate_hertz = 16000, language_code = "en-GB")
	streaming_config = speech.StreamingRecognitionConfig(config = config)
	answer = ""

	with open(path, "rb") as audio_file:
		stream = [audio_file.read()]
		requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in stream)
		
		# streaming_recognize returns a generator.
		responses = client.streaming_recognize(
			config = streaming_config,
			requests = requests,
		)

		for response in responses:
			for result in response.results:
				answer += result.alternatives[0].transcript

	return answer
			