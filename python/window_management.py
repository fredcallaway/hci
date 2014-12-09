#!/usr/bin/python

from Tkinter import *
import ScrolledText

class MainFrame(Frame):

    def __init__(self, parent, width=500, height=800):
        Frame.__init__(self,parent,relief=RAISED,borderwidth=2)
        self.parent=parent


        self.parent.geometry('%dx%d+200+100'%(width,height))
        self.pack(fill=BOTH,expand=1)

        hCanvas=int(round(height*0.625))

        self.canvas = Canvas(self,width=width,height=hCanvas,background='white')
        self.canvas.pack(fill=BOTH,expand=1)

        #note that the below elements may end up being truncated off if there
        #is insufficient height for the window
        self.entry = Entry(self,bd=2,background='old lace')
        self.entry.pack(fill=X,expand=1)

        self.text = ScrolledText.ScrolledText(self,bd=2,height=8,background='linen',undo=True)
        self.text.pack(fill=BOTH,expand=1)
        self.text.tag_config("usr", foreground="black")
        self.text.tag_config("app", foreground="dark green")
        self.text.tag_config("err", foreground="red")
