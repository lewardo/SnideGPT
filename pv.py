import wave, struct, tempfile
from decouple import config

from pvrecorder import PvRecorder as pvrecorder
import pvporcupine, pvcobra

recorder = pvrecorder(frame_length=512, device_index=0)

cobra = pvcobra.create(access_key=config('PICOVOICE_API_KEY'))
porcupine = pvporcupine.create(
	access_key=config('PICOVOICE_API_KEY'),
	keyword_paths=['./models/yobro.ppn']
)

def deinit():
	recorder.stop()
	recorder.delete()

def record_command(path):		
	recorder.start()
		
	command = []
	frame = recorder.read()

	print('waiting...')

	keyword_index = porcupine.process(frame)
	while keyword_index < 0:
		frame = recorder.read()
		keyword_index = porcupine.process(frame)
    
	print('listening...')

	voice_probability = cobra.process(frame)
	while voice_probability < 0.8:
		frame = recorder.read()
		voice_probability = cobra.process(frame)

		command.extend(frame)

	patience = 20
	streak = False

	while patience:
		frame = recorder.read()
		voice_probability = cobra.process(frame)

		if voice_probability < 0.1:
			if streak:
				patience -= 1
			else:
				streak = True
		else:
			patience = 20
			streak = False

		command.extend(frame)
	
	recorder.stop()

	with wave.open(path, "wb") as audio_file:
		audio_file.setparams((1, 2, 16000, 512, "NONE", "NONE"))
		audio_file.writeframes(struct.pack("h" * len(command), *command))
