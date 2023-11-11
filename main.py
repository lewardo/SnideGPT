import os, tempfile
import pv, gpt, stt, tts

if __name__ == "__main__":
    rec_fd, rec_path = tempfile.mkstemp(prefix = "snidegpt_rec_")
    spk_fd, spk_path = tempfile.mkstemp(prefix = "snidegpt_spk_")

    try:
        while True:
            pv.record_command(rec_path)

            print("processing...")

            transcription = stt.transcribe_file(rec_path)
            completion = gpt.get_completion(transcription)

            tts.generate_speech(completion, spk_path)
            tts.speak_file(spk_path)

            print('----------')

    except KeyboardInterrupt:
        pass

    finally:
        pv.deinit()

