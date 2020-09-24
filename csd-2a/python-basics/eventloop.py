# Notes from class on September 22nd, 2020
import simpleaudio as sa
import time as t

snare_event = {
    'timestamp': 100,
    'instrument': 'snare'
}

sequence = []

# Python does not create copies of a dictionary, but references it
for i in range(4):
    sequence.append(snare_event)

# To copy a dict, use .copy() (shallow copy)
snare_event2 = snare_event.copy()
snare_event2['timestamp'] = 200


def note_event_handler(event):
    print(event['instrumentName'])
    event['instrument'].play()


def create_event(timestamp, instrument, instrument_name):
    event = {
        'timestamp': timestamp,
        'instrument': instrument,
        'instrumentName': instrument_name,
        'note': "NA",
        'percussive': True,
        'duration': 500,
        'velocity': 30
    }
    return event


sequence = []
continueFlag = True
note_duration = 200

kick = sa.WaveObject.from_wave_file('../../assets/kick.wav')
snare = sa.WaveObject.from_wave_file('../../assets/snare.wav')

sequence.append(create_event(0, kick, 'Kick'))


class Threader:
    def __init__(self):
        self.sequence = sequence

    def run(self):
        tmpsequence = list(self.sequence)
        while continueFlag:
            event = tmpsequence.pop(0)
            ts = event['timestamp']

            timeZero = t.time() * 1000

            while True:
                now = t.time() * 1000
                if now - timeZero >= ts*note_duration:
                    play_obj = event['instrument'].play()
                    if tmpsequence:
                        event = tmpsequence.pop(0)
                        ts=event['timestamp']
                    else:
                        break
                else:
                    t.sleep(0.01)

            tmpsequence = list(self.sequence)
