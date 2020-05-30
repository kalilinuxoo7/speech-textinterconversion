import speech_recognition as sr

text_file = open('speech2text.txt', 'a', encoding='utf-8')
r = sr.Recognizer()
while True:
    with sr.Microphone() as source:
        print("Say something in hindi")
        # r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source, phrase_time_limit=3)
    print("fetching")
    try:
        x=r.recognize_google(audio,None,"hi")#.lower()
        print(x)
        if (x == 'एग्जिट'):
            break
        text_file.write(x + '\n')
    except sr.UnknownValueError:
        print("Could not understand audio")
        continue
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))
        continue


text_file.close()