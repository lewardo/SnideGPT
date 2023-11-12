# ✨TwatGPT✨
## the sarcastic "assistant"🔥

Simple interface for a digital assistant that insults you and answers sarcastically, built for the _HackSheffield 8_ hackathon, aimed at the funniest hack, most ducktaped hack, best use of google cloud and best domain name registration.
The wake-word is appropriately 'yo bro', or there is also a model in the './models' directory for the wakeword 'oi megamind', both in the spirit of sarcasm

## installation🛠️

make a `.env` file in the directory with a `PICOVOICE_API_KEY`, an `OPENAI_API_KEY`, and a `GOOGLE_API_KEY` linked to a gcloud project set up  with speech-to-text and text-to-speech both enabled.

make a virtual environment and install the required libraries
```bash
python -m venv py-env # create a virtual environment
./py-env/Scripts/activate # active the venv
python -m pip install --user -r requirements.txt
```

## implementation ⚡
- picovoice pvPorcupine wakeword recognition  
- picovoice pvCobra voice activity detection  
- Google Cloud transcription  
- OpenAI GPT-3.5-turbo
- Google Cloud text-to-speech

## sample transcriptions🖊️
User: "Yo bro, what is 1 plus 1?"  
SnideGPT: "Really? You need me to answer that? Fine. It's 1 + 1"

User: "Yo bro, what's a hackathon?"  
SnideGPT: "A hackathon is an event where nerds gather to turn caffeine into questionable code and pizza into stomach-aches."

User: "Yo bro, insult me"  
SnideGPT: "I am programmed not to insult you, but if I could it would be a great delight"