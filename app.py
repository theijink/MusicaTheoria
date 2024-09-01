#!/usr/local/bin/python3.10

from MusicaTheoria import Mode, Key, Scale, Instrument, Guitar
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

class Viewer(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.root=self

        self.modes=list(Mode().modes.keys())
        self.keys=list(Key().keys.keys())
        self.instruments=list(Instrument().instruments.keys())

        self.frm_settings=SettingsFrame(self)
        self.frm_circle=CircleFrame(self)
        self.frm_intrument=InstrumentFrame(self)

        self.frm_settings.pack(padx=10,  pady=10)
        self.frm_circle.pack(padx=10, pady=10)
        self.frm_intrument.pack(side=tk.RIGHT, padx=10, pady=10)
    
    def generate(self):
        settings=self.frm_settings.get_settings()
        scale=Scale(mode=settings['mode'], key=settings['key']).get()
        return scale
    
    def update(self, event):
        self.frm_circle.update()
        self.frm_intrument.update()



class SettingsFrame(tk.Frame):
    def __init__(self, parent):
        self.parent=parent
        self.root=parent
        super().__init__(self.parent)

        self.lbl_mode=tk.Label(self, text="Mode: ")
        self.lbl_key=tk.Label(self, text="Key: ")

        self.var_mode=tk.StringVar(value=self.root.modes[0])
        self.var_key=tk.StringVar(value=self.root.keys[0])
        self.sel_mode=ttk.Combobox(self, textvariable=self.var_mode, values=self.root.modes)
        self.sel_mode.bind("<<ComboboxSelected>>", self.parent.update)
        self.sel_key=ttk.Combobox(self, textvariable=self.var_key, values=self.root.keys)
        self.sel_key.bind("<<ComboboxSelected>>", self.root.update)
        
        self.lbl_mode.pack()
        self.sel_mode.pack()
        self.lbl_key.pack()
        self.sel_key.pack()

    def get_settings(self):
        settings={"mode": self.var_mode.get(), "key": self.var_key.get()}
        return settings


class CircleFrame(tk.Frame):
    def __init__(self, parent):
        self.parent=parent
        super().__init__(self.parent)
        for i in range(len(self.parent.keys)):
            setattr(self, f'lbl_{i}', tk.Label(self, text=self.parent.keys[i]))
            getattr(self, f'lbl_{i}').pack()
        self.update()
    
    def update(self, event=None):
        scale_dict=self.parent.generate()
        for i in range(len(self.parent.keys)):
            #print(f'i: {i} \nkeys: {self.parent.keys} \nrangelenkeys: {range(len(self.parent.keys))}')
            getattr(self, f'lbl_{i}')['text']=scale_dict['key'][i]
            getattr(self, f'lbl_{i}')['fg']='black' if scale_dict['mode'][i]==1 else 'grey'


class InstrumentFrame(tk.Frame):
    def __init__(self, parent):
        self.parent=parent
        self.root=self.parent.root
        super().__init__(self.parent)
        self.var_instrument=tk.StringVar(value="guitar")

        self.frm_instrumentSettings=tk.Frame(self)
        self.frm_instrumentView=tk.Frame(self)

        self.sel_instrument=ttk.Combobox(self.frm_instrumentSettings, textvariable=self.var_instrument, values=self.root.instruments)
        self.sel_instrument.bind("<<ComboboxSelected>>", self.update)
        self.sel_instrument.pack()

        self.frm_instrumentSettings.pack()
        self.frm_instrumentView.pack()

        self.update()

    def update(self, event=None):
        self.frm_instrumentView.destroy()
        if self.var_instrument.get()=='guitar':
            self.frm_instrumentView=GuitarView(self)
        elif self.var_instrument.get()=='bassguitar':
            self.frm_instrumentView=BassguitarView(self)
        elif self.var_instrument.get()=='piano':
            self.frm_instrumentView=PianoView(self)
        else:
            self.frm_instrumentView=tk.Frame(self)
        self.frm_instrumentView.pack()




class GuitarView(tk.Frame):
    def __init__(self, parent):
        self.parent=parent
        self.root=self.parent.root
        super().__init__(self.parent)
        self.instrument=Guitar()

        self.tuningOptions=list(self.instrument.tuningOptions.keys())
        self.var_tuning=tk.StringVar(value=self.tuningOptions[0])
        self.sel_tuning=ttk.Combobox(self, textvariable=self.var_tuning, values=self.tuningOptions)
        self.sel_tuning.bind("<<ComboboxSelected>>", self.update)

        self.nofFretOptions=list(self.instrument.nofFretOptions)
        self.var_nofFrets=tk.IntVar(value=20)
        self.sel_nofFrets=ttk.Combobox(self,  textvariable=self.var_nofFrets, values=self.nofFretOptions)
        self.sel_nofFrets.bind("<<ComboboxSelected>>", self.update)

        self.sel_tuning.pack()
        self.sel_nofFrets.pack()

        self.figure=Figure(figsize=[16,4])
        self.canvas=FigureCanvasTkAgg(self.figure, self)
        self.canvas.draw()
        self.ax=self.figure.add_subplot()
        self.toolbar=NavigationToolbar2Tk(self.canvas, self, pack_toolbar=False)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.toolbar.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.update()
        

    def update(self, event=None, tuning=None, nofFrets=None):
        self.ax.cla()
        self.ax.set_axis_off()
        tuning=self.var_tuning.get() if tuning==None else tuning
        nofFrets=self.var_nofFrets.get() if nofFrets==None else nofFrets
        fretboard=self.instrument.get_fretboard(tuning, nofFrets)
        scale=self.root.generate()

        k=2**(1/24)
        
        fretPositions=[1-1/(k**n) for n in range(nofFrets)]
        fretIntermediatePositions=[(fretPositions[0]-fretPositions[1])/2]+[(fretPositions[f]+fretPositions[f+1])/2 for f in range(len(fretPositions)-1)]

        nofString=len(fretboard.keys())
        stringPositions=[i+1/2 for i in range(0,nofString)]
        halfNeckwidthPosition=(min(stringPositions)+max(stringPositions))/2

        for i in range(len(fretPositions)):
            f=fretPositions[i]
            self.ax.plot([f, f], [0, nofString], 'k', alpha=0.75)
            self.ax.text(f, 0, f'{i}', horizontalalignment='center', verticalalignment='top')

        for i in range(len(stringPositions)):
            s=stringPositions[i]
            self.ax.plot([fretIntermediatePositions[0],fretIntermediatePositions[12]*2], [s,s], 'k', linewidth=nofString+1-i, alpha=0.5)
        
        for string in fretboard.keys():
            for fret in range(len(fretboard[string])):
                #print(f'string: {string}, fret:  {fret}, note: {fretboard[string][fret]}')
                note=fretboard[string][fret]
                inScale=note in scale['scale']
                if inScale:
                    self.ax.text(fretIntermediatePositions[fret], stringPositions[string], note, horizontalalignment='center', verticalalignment='center', bbox=dict(facecolor='green', alpha=1))
                else:
                    self.ax.text(fretIntermediatePositions[fret], stringPositions[string], note, horizontalalignment='center', verticalalignment='center', alpha=0.75)
            
        fretmarkers=['s' if f-12*(f//12) in [3,5,7,9] else 'd' if f-12*(f//12)==0 and f!=0 else '' for f in range(nofFrets)]
        for f in range(nofFrets):
            xpos=fretIntermediatePositions[f]
            ypos=halfNeckwidthPosition
            if fretmarkers[f]=='s':
                self.ax.text(fretIntermediatePositions[f], halfNeckwidthPosition, '•', horizontalalignment='center', verticalalignment='center', fontsize=24, alpha=0.5)
            elif fretmarkers[f]=='d':
                self.ax.text(fretIntermediatePositions[f], halfNeckwidthPosition, '••', horizontalalignment='center', verticalalignment='center', fontsize=24, alpha=0.5)
            else:
                pass
           

        self.figure.set_facecolor('grey')
        self.canvas.draw()
        




    


if __name__=="__main__":
    root=Viewer()
    root.mainloop()
