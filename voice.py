#!/usr/bin/env python3
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer, SetLogLevel
import json
import threading

SetLogLevel(-1)

q = queue.Queue()
_lock = threading.Lock()

model = Model(lang='en-us')
record = KaldiRecognizer(model, 16000)
record.SetWords(True)

# Only final (AcceptWaveform) results are used for yes/no decisions.
# Partial results update _spoken_partial for display only.
_spoken_final   = None   # last confirmed final utterance
_spoken_partial = None   # last partial (display only, never used for decisions)
stfu = False

# ---------------------------------------------------------------------------
# Word lists — scored by confidence tier
# Tier 1 words win immediately; Tier 2 words win only if no Tier 1 word
# matched on the other side.
# ---------------------------------------------------------------------------
YES_T1 = {'yes', 'yeah', 'yep', 'yup', 'sure', 'okay', 'ok',
           'absolutely', 'correct', 'right', 'affirmative', 'indeed',
           'please', 'yea', 'aye'}
YES_T2 = {'maybe', 'fine', 'alright', 'yesh', 'mhm'}

NO_T1  = {'no', 'nope', 'nah', 'never', 'negative', 'stop',
           'quit', 'dont', "don't", 'refuse', 'decline', 'nay'}
NO_T2  = {'not'}

def _classify(text: str):
    """Return 'yes', 'no', or None from a final transcript."""
    words = set(text.lower().split())
    has_yes_t1 = bool(words & YES_T1)
    has_yes_t2 = bool(words & YES_T2)
    has_no_t1  = bool(words & NO_T1)
    has_no_t2  = bool(words & NO_T2)

    yes_score = (2 if has_yes_t1 else 0) + (1 if has_yes_t2 else 0)
    no_score  = (2 if has_no_t1  else 0) + (1 if has_no_t2  else 0)

    if yes_score == 0 and no_score == 0:
        return None
    return 'yes' if yes_score >= no_score else 'no'


def yn():
    """
    Check the last confirmed spoken utterance for a yes/no answer.
    Returns 'yes', 'no', or None.
    Must only be called from speaker_talk_thrd.
    """
    global _spoken_final, stfu
    with _lock:
        if stfu:
            _spoken_final = None
            return None
        text = _spoken_final
    if text is None:
        return None
    result = _classify(text)
    if result is not None:
        print(f'[voice] yn={result!r} from {text!r}')
    return result


def resetspoken():
    global _spoken_final, _spoken_partial
    with _lock:
        _spoken_final   = None
        _spoken_partial = None


def stfugng():
    global stfu
    with _lock:
        stfu = True
        _spoken_final = None


def unstfugng():
    global stfu
    with _lock:
        stfu = False


# ---------------------------------------------------------------------------
# Audio callback — runs in the sounddevice thread
# ---------------------------------------------------------------------------
def _audio_callback(indata, _frames, _time, _status):
    if not stfu:
        q.put(bytes(indata[::3, :]))


# ---------------------------------------------------------------------------
# Background thread — feeds audio into Vosk
# ---------------------------------------------------------------------------
def detect():
    global _spoken_final, _spoken_partial
    with sd.InputStream(device=1, samplerate=48000, blocksize=8000,
                        dtype='int16', channels=1, callback=_audio_callback):
        print('[voice] microphone open')
        while True:
            data = q.get()
            if stfu:
                with _lock:
                    _spoken_final = None
                continue

            if record.AcceptWaveform(data):
                result = json.loads(record.Result())
                text   = result.get('text', '').strip()
                if text:
                    print(f'[voice] final: {text!r}')
                    with _lock:
                        _spoken_final = text
            else:
                partial = json.loads(record.PartialResult()).get('partial', '')
                with _lock:
                    _spoken_partial = partial
                print(partial, end='\r')
