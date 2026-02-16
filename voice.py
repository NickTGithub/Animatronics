#!/usr/bin/env python3 
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer, SetLogLevel
import json
from downsample import downsample_audio

SetLogLevel(-1)

q = queue.Queue()

model = Model(lang='en-us')
record = KaldiRecognizer(model, 16000)
record.SetWords(True)

spoken = ''

#a, b, c just placeholders that do nothing bc we dont need to use them
#throws sound files in queue to be used
def audio_callback(indata, a, b, c):
    global stfu, spoken
    if stfu == False:
        downData = indata[::3, :]
        q.put(bytes(downData))
    else:
        spoken = None

yeslist = ['yes','yeah','maybe','yay','ok','okay','yesh']
nolist = ['no']
output = 'maybe'
tryYN = False

def yn():
    global spoken, yeslist, nolist, output, stfu, result, tryYN
    output = None
    if stfu == True:
        spoken = None
        output = None
        result = 'none'
    else:
        found = False
        if spoken != None and tryYN == True:
            #print('spoken',spoken)
            for i in yeslist:
                if i in spoken and found == False:
                    output = 'yes heard'
                    print('output',output)
                    found = True
                    print('yes found in', spoken)
            for i in nolist:
                if i in spoken and found == False:
                    output = 'no heard'
                    print('output',output)
                    found = True
                    print('no found in', spoken)
        if output == 'yes heard':
            result = 'yes'
            print('yes found in', spoken)
        elif output == 'no heard':
            result = 'no'
        else:
            result = 'none'
    output = None
    return result

def resetspoken():
    global spoken, output
    spoken = None
    output = None

stfu = False

def stfugng():
    global stfu
    stfu = True

def unstfugng():
    global stfu
    stfu = False

def detect():
    global spoken, yeslist, nolist, output, tryYN
    #gets raw imput from microphone
    with sd.InputStream(device=1,samplerate=48000, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
        print('go')
        while True:
        
            #get next file in queue
            data = q.get()

            tryYN = False

            #if model is confident, print result, otherwise print best guess
            if record.AcceptWaveform(data) == True:
                result = json.loads(record.Result())
                spoken = result.get('text')
                print('spoken',spoken)
                tryYN = True
            else:
                partial = json.loads(record.PartialResult())
                spoken = partial.get('partial', '')
                print(spoken, end='\r')

            if stfu == True:
                spoken = None
                
            
                

            

