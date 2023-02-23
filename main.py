import os 
import openai
from dotenv import load_dotenv
import speech_recognition as sr
load_dotenv()


# print(completion.choices[0].text[2:])



def recognize_speech(recognizer, microphone):
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")
    
    with microphone as source: 
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True,
        "error": None
    }

    try:
        data = recognizer.recognize_google(audio, show_all=True)

    except sr.RequestError:
        response["error"] = "API unavailable"
        response["success"] = False

    except sr.UnknownValueError:
        response["error"] = "Unable to detect speech" 
    
    if response["success"]:
        return data["alternative"][0]["transcript"]
    


openai.api_key = os.getenv("OPENAI_API_KEY")

completion = openai.Completion.create(model="text-davinci-003", prompt = f"This is a conversation with a chatrobot named charlie. Me:{recognize_speech(sr.Recognizer(), sr.Microphone())}. Charlie: ", max_tokens=2000)

print(completion.choices[0].text[2:])