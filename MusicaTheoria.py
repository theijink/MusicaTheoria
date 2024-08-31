
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




if __name__=="__main__":
    mode=Mode(mode='ionian')
    key=Key(key='C')

    scale=[key.get()[i] if mode.get()[i]==1 else None for i in range(len(mode.get()))]
    while None in scale: scale.remove(None)
    
    print(scale)