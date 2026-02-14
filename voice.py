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
newWord = False

#a, b, c just placeholders that do nothing bc we dont need to use them
#throws sound files in queue to be used
def audio_callback(indata, a, b, c):
    downData = indata[::3, :]
    q.put(bytes(downData))

yeslist = ['yes','yeah','maybe','yay','ok','okay']
nolist = ['no']
output = 'maybe'
running = False
tryYN = False

def yn():
    global spoken, yeslist, nolist, output, running, tryYN
    found = False
    if tryYN == True:
        for i in yeslist:
            if i in spoken and found  == False:
                output = 'yes heard'
                print(output)
                found = True
        for i in nolist:
            if i in spoken and found  == False:
                output = 'no heard'
                print(output)
                found = True
    if output == 'yes heard':
        result = 'yes'
    elif output == 'no heard':
        result = 'no'
    else:
        result = 'none'
    return result

def resetspoken():
    global spoken
    spoken = 'fjiaeorgioe'

stfu = False

def stfugng():
    global stfu
    stfu = True

def unstfugng():
    global stfu
    stfu = False

def detect():
    global spoken, newWord, yeslist, nolist, output, running, tryYN
    #gets raw imput from microphone
    with sd.InputStream(device=1,samplerate=48000, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
        print('go')
        while True:
        
            #get next file in queue
            tryYN = False
            spoken = 'yf'
            data = q.get()

            #if model is confident, print result, otherwise print best guess
            if record.AcceptWaveform(data) == True:
                tryYN = True
                result = json.loads(record.Result())
                #print(result.get('text'))
                if stfu == True:
                    spoken = 'gheauigh'
                else:
                    spoken = result.get('text')
                print(spoken)
                
            else:
                partial = json.loads(record.PartialResult())
                #print(partial.get('partial', ''), end='\r')
                
                if stfu == True:
                    spoken = 'gheauigh'
                else:
                    spoken = partial.get('partial', '')
                print(spoken, end='\r')
            
                
            
                

            

