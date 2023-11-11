# ✨SnideGPT✨
## the sarcastic assistant

Simple interface for a digital assistant that insults you and answers sarcastically, built for the HackSheffield 8 hackathon

## installation

make a `.env` file in the directory with a `PICOVOICE_KEY` from a free picovoice account, and make sure you have `OPENAI_API_KEY` defined in your environment variables to access the openai API, and make sure you have gcloud set up enabling a project with speech-to-text and text-to-speech both enabled.

make a virtual environment and install the required libraries
```bash
python -m venv py-env # create a virtual environment
./py-env/Scripts/activate # active the venv
python -m pip install -r requirements.txt
```

---

## implementation ⚡
- picovoice pvporcupine wakeword recognition  
- picovoice pvcobra voice activity detection  
- google cloud transcription  
- openai gpt 3.5 turbo
- google cloud text to speech
