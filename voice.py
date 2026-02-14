#!/usr/bin/env python3 
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer, SetLogLevel
import json

SAMPLE_RATE = 16000

SetLogLevel(-1)

q = queue.Queue()

model = Model(lang='en-us')
record = KaldiRecognizer(model, SAMPLE_RATE)
record.SetWords(True)

spoken = ''
newWord = False

#a, b, c just placeholders that do nothing bc we dont need to use them
#throws sound files in queue to be used
def audio_callback(indata, a, b, c):
    q.put(bytes(indata))

yeslist = ['yes']
nolist = ['no']
output = 'maybe'
running = False

def yn():
    global spoken, yeslist, nolist, output, running
    if spoken in yeslist:
        output = 'yes heard'
        print(output)
    elif spoken in nolist:
        output = 'no heard'
        print(output)


def detect():
    global spoken, newWord, yeslist, nolist, output, running
    #gets raw imput from microphone
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):

        while True:
            #get next file in queue

            data = q.get()

            #if model is confident, print result, otherwise print best guess
            if record.AcceptWaveform(data) == True:
                result = json.loads(record.Result())
                #print(result.get('text'))
                spoken = result.get('text')
                print(spoken)
                
            else:
                partial = json.loads(record.PartialResult())
                #print(partial.get('partial', ''), end='\r')
                spoken = partial.get('partial', '')
                print(spoken, end='\r')
            
                

            

