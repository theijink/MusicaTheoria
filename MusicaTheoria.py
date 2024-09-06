
class Measure():
    def __init__(self) -> None:
        ## measures, bars or timesignatures. The first number deflects how many beats there are per measure/bar, the second number tells what note is beating.
        self.measures=['2/4', '3/4', '4/4', '6/8']

    def get(self):
        return self.measures

class Division():
    def __init__(self) -> None:
        ## division of the timeline 
        self.divisions={
            'semibreve': 1/1,
            'minims': 1/2,
            'crotchets': 1/4,
            'quavers': 1/8,
            'semiquavers': 1/16,
            'demisemiquavers': 1/32
        }

    def get(self):
        return self.divisions


class Key():
    def __init__(self, key=None) -> None:
        self.keys={'C':0, 'C♯/D♭':1, 'D':2, 'D♯/E♭':3, 'E':4, 'F':5, 'F♯/G♭':6, 'G':7, 'G♯/A♭':8, 'A':9, 'A♯/B♭':10, 'B':11}
        self.set(key=key)

    def set(self, key=None):
        if key in self.keys.keys():
            ind=self.keys[key]
            seq=list(self.keys.keys())[ind:]+list(self.keys.keys())[:ind]
        else:
            seq=['X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X']
        self.selected_keys=seq

    def get(self):
        return self.selected_keys




class Mode():
    def __init__(self, mode=None) -> None:
        self.base='WWHWWWH'
        self.modes={
            'ionian': self.base,
            'dorian': self.base[1:]+self.base[:1],
            'phrygian': self.base[2:]+self.base[:2],
            'lydian': self.base[3:]+self.base[:3],
            'mixolydian': self.base[4:]+self.base[:4],
            'aeolian': self.base[5:]+self.base[:5],
            'locrian': self.base[6:]+self.base[:6]
        }
        self.set(mode)

    def set(self, mode):
        if mode in self.modes.keys():
            self.selected_mode={'name': mode, 'intervals': self.modes[mode]}
        else:
            self.selected_mode={'name': 'undefined', 'intervals': 'NNNNNNNNNNNN'}
    
    def get(self):
        str=self.selected_mode['intervals'].replace('W','10').replace('H','1').replace('N','0')
        seq=[int(i) for i in str]
        return seq


class Scale():
    def __init__(self, mode=None, key=None) -> None:
        self.mode=Mode(mode=mode)
        self.key=Key(key=key)
    
    def get(self):
        scale=[self.key.get()[i] if self.mode.get()[i]==1 else None for i in range(len(self.mode.get()))]
        while None in scale: scale.remove(None)
        return {'key':self.key.get(), 'mode':self.mode.get(), 'scale':scale}


class Instrument():
    def __init__(self, instrument=None) -> None:
        self.instruments={
                'guitar': Guitar,
                'bassguitar': BassGuitar,
                'piano': KeyInstrument
        }


class StringInstrument(Instrument):
    def __init__(self, instrument=None) -> None:
        super().__init__(instrument)

    def get_fretboard(self, tuning=None, nof_frets=None):
        if not tuning==None and not nof_frets==None:
            pass




class KeyInstrument(Instrument):
    def __init__(self, instrument=None) -> None:
        super().__init__(instrument)



class Guitar(StringInstrument):
    def __init__(self, instrument='guitar') -> None:
        super().__init__(instrument)
        self.tuningOptions={
            'standard_6_string': ['E', 'A', 'D', 'G', 'B', 'E']
        }
        self.nofFretOptions=list(range(13,30))

    def get_fretboard(self, tuning=None, nof_frets=None):
        fretboard={t: [Scale(key=self.tuningOptions[tuning][t]).get()['key'][f] for f in [f-(12*(f//12)) for f in range(0,nof_frets)]] for t in range(len(self.tuningOptions[tuning]))}
        return fretboard




class BassGuitar(StringInstrument):
    def __init__(self, instrument='bassguitar') -> None:
        super().__init__(instrument)
        self.tuningOptions={
            'standard_4_string': ['E', 'A', 'D', 'G'],
            'standard_5_string': ['B', 'E', 'A', 'D', 'G'],
            'standard_6_string': ['B', 'E', 'A', 'D', 'G', 'C']
        }

class Piano(KeyInstrument):
    def __init__(self, instrument='piano') -> None:
        super().__init__(instrument)



if __name__=="__main__":
    mode=Mode(mode='ionian')
    key=Key(key='C')

    scale=[key.get()[i] if mode.get()[i]==1 else None for i in range(len(mode.get()))]
    while None in scale: scale.remove(None)
    
    print(scale)