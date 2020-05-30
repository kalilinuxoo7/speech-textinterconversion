from vosk import Model, KaldiRecognizer
import os,json

if not os.path.exists("model"):
    print ("Please download the model and unpack as 'model' in the current folder.")
    exit (1)

import pyaudio
text_file = open('speech2textoffline.txt', 'a')
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

model = Model("model")
rec = KaldiRecognizer(model, 16000)

while True:
    data = stream.read(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())
        a=rec.Result()
        b=json.loads(a)
        print('b.text is',b['text'])
        resultfinal = b['text']
        text_file.write(resultfinal+'\n')
        if(resultfinal =='exit'):
            break
    else:
        print(rec.PartialResult())

print("final", rec.FinalResult())

text_file.close()