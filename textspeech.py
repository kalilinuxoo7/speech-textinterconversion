import pyttsx3

# One time initialization
engine = pyttsx3.init()

# Set properties _before_ you add things to say
engine.setProperty('rate', 150)    # Speed percent (can go over 100)
engine.setProperty('volume', 0.9)  # Volume 0-1
print('Dictating text2speech.txt')
# Queue up things to say.
# There will be a short break between each one
# when spoken, like a pause between sentences.
file = open('text2speech.txt', 'r')
text = file.read()
file.close()
engine.say(text)
# for voice in voices:
#     print("Voice:")
#     print(" - ID: %s" % voice.id)
#     print(" - Name: %s" % voice.name)
#     print(" - Languages: %s" % voice.languages)
#     print(" - Gender: %s" % voice.gender)
#     print(" - Age: %s" % voice.age)
#Flush the say() queue and play the audio
engine.runAndWait()
