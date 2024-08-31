#!/usr/local/bin/python3.10

from draft import Mode, Key
import tkinter as tk
from tkinter import ttk

class Viewer(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        self.modes=list(Mode().modes.keys())
        self.keys=list(Key().keys.keys())


        self.var_mode=tk.StringVar(value=self.modes[0])
        self.var_key=tk.StringVar(value=self.keys[0])

        self.frm_circle=CircleFrame(self)
        self.sel_mode=ttk.Combobox(self, textvariable=self.var_mode, values=self.modes)
        self.sel_mode.bind("<<ComboboxSelected>>", self.frm_circle.update)
        self.sel_key=ttk.Combobox(self, textvariable=self.var_key, values=self.keys)
        self.sel_key.bind("<<ComboboxSelected>>", self.frm_circle.update)
        
        self.sel_mode.pack()
        self.sel_key.pack()
        self.frm_circle.pack()
    
    def generate(self):
        self.val_mode=self.var_mode.get()
        self.val_key=self.var_key.get()
        mode=Mode(mode=self.val_mode)
        key=Key(key=self.val_key)
        scale=[key.get()[i] if mode.get()[i]==1 else None for i in range(len(mode.get()))]
        while None in scale: scale.remove(None)
        return {'key':key.get(), 'mode':mode.get(), 'scale':scale}

    

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
            getattr(self, f'lbl_{i}')['text']=scale_dict['key'][i]
            getattr(self, f'lbl_{i}')['fg']='black' if scale_dict['mode'][i]==1 else 'grey'


if __name__=="__main__":
    root=Viewer()
    root.mainloop()