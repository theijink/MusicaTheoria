#!/usr/local/bin/python3.10

from MusicaTheoria import Mode, Key, Scale, Instrument, Guitar
from customtkinter import CTk, CTkFrame, StringVar, IntVar, CTkLabel, CTkComboBox, CTkButton
import tkinter as tk
import datetime as dt

def log(lvl,msg):
    print(f"{dt.datetime.now()} [{lvl}]{' '*(10-max(0,len(lvl)))}: {msg}")


class SettingsColumn(CTkFrame):
    def __init__(self, parent):
        self.parent=parent
        self.root=self.parent.root
        super().__init__(self.parent)
        ## mode item
        self.mode=LabelComboboxFrame(self, labelname='mode', variablevalue=self.root.modes[0], comboboxvalues=self.root.modes)
        self.mode.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=self.root.padxValue, pady=self.root.padyValue)
        ## key item
        self.key=LabelComboboxFrame(self, labelname='key', variablevalue=self.root.keys[0], comboboxvalues=self.root.keys)
        self.key.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=self.root.padxValue, pady=self.root.padyValue)
        ## scale item ??
        ## extentions ??
    


class LabelComboboxFrame(CTkFrame):
    def __init__(self, parent, labelname='label', variablevalue=None, comboboxvalues=[]):
        self.parent=parent
        self.root=self.parent.root
        super().__init__(self.parent)
        self.var=StringVar(self, value=variablevalue)    
        self.lbl=CTkLabel(self, text=labelname)
        self.cmx=CTkComboBox(self, variable=self.var, values=comboboxvalues)
        self.cmx.bind("<<ComboboxSelected>>", lambda event:self.root.update())
        self.lbl.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=self.root.padxValue, pady=self.root.padyValue)
        self.cmx.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=self.root.padxValue, pady=self.root.padyValue)







class GraphicsColumn(CTkFrame):
    def __init__(self, parent):
        self.parent=parent
        self.root=self.parent.root
        super().__init__(self.parent)
        self.instrumentFrames=[]
        self.btn_addInstrument=CTkButton(self, text="+", command=lambda:self.add_instrument())
        self.btn_addInstrument.pack(side=tk.TOP, fill=tk.NONE, expand=False, padx=self.root.padxValue, pady=self.root.padyValue)

    
    def add_instrument(self):
        self.instrumentFrames.append(InstrumentFrame(self))
        self.instrumentFrames[-1].pack(side=tk.TOP, fill=tk.X, expand=True, padx=self.root.padxValue, pady=self.root.padyValue)
        self.instrumentFrames[-1].update()


class InstrumentFrame(CTkFrame):
    def __init__(self, parent):
        self.parent=parent
        self.root=self.parent.root
        super().__init__(self.parent)
        log('INFO', 'initiated instrumentFrame')
        ## instrument
        self.instrument=LabelComboboxFrame(self, labelname='instrument', variablevalue=self.root.instruments[0], comboboxvalues=self.root.instruments)
        self.instrument.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=self.root.padxValue, pady=self.root.padyValue)
        ## destroy
        self.btn_destroy=CTkButton(self.instrument, text="x", command=lambda:self.destroy())
        self.btn_destroy.pack(side=tk.RIGHT, fill=tk.NONE, expand=False, padx=self.root.padxValue, pady=self.root.padyValue)
        ## settings
        self.settingsFrame=CTkFrame(self)
        self.settingsFrame.pack(side=tk.TOP, fill=tk.X, expand=True, padx=self.root.padxValue, pady=self.root.padyValue)
        ## graphics
        self.graphicsFrame=CTkFrame(self)
        self.graphicsFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=self.root.padxValue, pady=self.root.padyValue)
        ## update
        #self.update()

    def update(self, event=None):
        self.settingsFrame.destroy()
        self.graphicsFrame.destroy()
        log('INFO', f"instrument selected: {self.instrument.var.get()}")
        if self.instrument.var.get()=='guitar':
            self.settingsFrame=GuitarSettingsFrame(self)
            log('INFO', f"settingsFrame created for instrument {self.instrument.var.get()}")
            self.graphicsFrame=GuitarGraphicsFrame(self)
            log('INFO', f"graphicsFrame created for instrument {self.instrument.var.get()}")
        elif self.instrument.var.get()=='bassguitar':
            log('INFO', f"skip creating frames for instrument {self.instrument.var.get()}")
        elif self.instrument.var.get()=='piano':
            log('INFO', f"skip creating frames for instrument {self.instrument.var.get()}")
        else:
            self.settingsFrame=CTkFrame(self)
            log('INFO', f"empty settingsFrame created for unknown instrument {self.instrument.var.get()}")
            self.graphicsFrame=CTkFrame(self)
            log('INFO', f"empty graphicsFrame created for unknown instrument {self.instrument.var.get()}")
        self.settingsFrame.pack(side=tk.TOP, fill=tk.X, expand=True, padx=self.root.padxValue, pady=self.root.padyValue)
        self.graphicsFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=self.root.padxValue, pady=self.root.padyValue)
        #self.settingsFrame.update()
        #self.graphicsFrame.update()
        



class GuitarSettingsFrame(CTkFrame):
    def __init__(self, parent):
        self.parent=parent
        self.root=self.parent.root
        super().__init__(self.parent)
        log('INFO', f"GuitarSettingsFrame initiated")
        self.instrument=Guitar()
        ## tuning
        self.tuningOptions=list(self.instrument.tuningOptions.keys())
        self.tuning=LabelComboboxFrame(self, labelname='tuning', variablevalue=self.tuningOptions[0], comboboxvalues=self.tuningOptions)
        self.tuning.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=self.root.padxValue, pady=self.root.padyValue)
        log('INFO', f"added tuning selection for GuitarSettingsFrame")
        ## nofFrets
        self.nofFretOptions=[str(i) for i in self.instrument.nofFretOptions]
        self.nofFrets=LabelComboboxFrame(self, labelname='nofFrets', variablevalue='20', comboboxvalues=self.nofFretOptions)
        self.nofFrets.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=self.root.padxValue, pady=self.root.padyValue)
        log('INFO', f"added nofFrets selection for GuitarSettingsFrame")
        


class GuitarGraphicsFrame(CTkFrame):
    def __init__(self, parent):
        self.parent=parent
        self.root=self.parent.root
        super().__init__(self.parent)
        log('INFO', f"GuitarGraphicsFrame initiated")
    
    def update(self, event=None):
        pass









class UtilityColumn(CTkFrame):
    def __init__(self, parent):
        self.parent=parent
        self.root=self.parent.root
        super().__init__(self.parent)




class App(CTk):
    def __init__(self):
        self.root=self
        super().__init__()
        super().title("MusicaTheoria")
        self.padxValue=10
        self.padyValue=10

        self.modes=list(Mode().modes.keys())
        self.keys=list(Key().keys.keys())
        self.instruments=list(Instrument().instruments.keys())

        self.settingsColumn=SettingsColumn(self)
        self.graphicsColumn=GraphicsColumn(self)
        self.utilityColumn=UtilityColumn(self)

        self.settingsColumn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=self.padxValue, pady=self.padyValue)
        self.graphicsColumn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=self.padxValue, pady=self.padyValue)
        self.utilityColumn.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=self.padxValue, pady=self.padyValue)

    def update(self):
        self.settingsColumn.update()
        self.graphicsColumn.update()
        self.utilityColumn.update()



if __name__=="__main__":
    root=App()
    root.mainloop()