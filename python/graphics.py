#!/usr/bin/python

from Tkinter import *
from window_management import MainFrame
from copy import deepcopy

#reference to the graphics canvas

canvas = None
def canvasHeight():
    return canvas.winfo_screenheight()
#TODO check this works
def canvasWidth():
    return canvas.winfo_screenwidth()
##TODO check this works
def standardSizes():
    return [100.0,100.0]

class Attributes(dict):
    def __init__(self,*args,**kw):
        super(Attributes,self).__init__(*args,**kw)
        #define special fields
        self.center=[0.0,0.0]
        self.span=standardSizes()
        self.idnum=None # tells us if the object has been drawn
        self.names=[]

x=Attributes()
x['color']='green'
x['color']
x.center=[1,1,1,1]


def relMove(attr,command):
    [x,y]=attr.center
    dh=canvasHeight() * 0.2
    dw=canvasWidth() * 0.2
    if command is 'up':
        attr.center=[x,y+dh]
    elif command is 'down':
        attr.center=[x,y-dh]
    elif command is 'left':
        attr.center=[x-dw,y]
    elif command is 'right':
        attr.center=[x+dw,y]
    else:
        return

def relSize(attr,command):
    [w,h] = attr.span
    if command is 'taller':
        h *= 1.3
    elif command is 'shorter':
        h /= 1.3
    elif command is 'wider':
        w *= 1.3
    elif command is 'narrower':
        w /= 1.3
    elif command is 'larger':
        w *= 1.3
        h *= 1.3
    elif command is 'smaller':
        w /= 1.3
        h /= 1.3
    else:
        return
    attr.span=[w,h]

def addName(attr,name):
    attr['names'].append(name)

#constants for specifying attributes that are absolute, ie enumerated
attrTypes = ('shape','size','positioning')
attrNames = (
    ('oval','circle','rectangle','square','triangle'),
    ('tall','short','wide','narrow','large','small'),
    ('top','bottom','left','right')
)
#note that color is a catch-all type for names that don't match the above lists

#constants for changing, relative absolutes
changeTypes = (relMove, relSize)
changeNames = (
    ('up','down','left','right'),
    ('taller','shorter','wider','narrower','larger','smaller')
)

#use this when updating Attributes
#ie make2
def updateAttributes(attr,command):
    #check for relative changes
    for i in range(len(changeTypes)):
        if command in changeNames[i]:
            changeTypes[i](attr,command)
            return
    #check for absolute changes
    setAttributes(attr, command)

#use this function when creating a new Attributes
#ie make1
def setAttributes(attr, command):
    for i in range(len(attrTypes)):
        if command in attrNames[i]:
            attr[attrTypes[i]]=command
            return
    #if the change name is not recognized, assume it's a color
    #this way we don't have to list every single color possible
    attr['color']=command


it = None
#TODO!! Think carefully about history. Need a good datastructure, linked 
#somehow to recreate previous images

class HistoryEntry:
    def __init__(self,attr):
        self.history = [deepcopy(attr)]
        self.current = 0
        self.total = 1
    def update(self,attr):
        self.history.append(deepcopy(attr))
        self.current += 1
        self.total = self.current+1 #erase Redos
    def undo(self):
        self.current -= 1
        if self.current < 0:
            self.current = 0
            return None
        return self.get()
    def redo(self):
        self.current += 1
        if self.current >= self.total:
            self.current = self.total-1
            return None
        return self.get()
    def get():
        return self.history[self.current]

class HistoryMap:
    def __init__(self):
        self.mappings={}
        self.newestID = -1
    def getNewID():
        self.newestID += 1
        return self.newestID
    def add(self,attr):
        #entry = self.mappings.get(attr.idnum,None)
        #if entry == None:
        self.mappings[getNewID()]=HistoryEntry(attr)
        #else:
        #    entry.update(attr)
        return self.newestID
    def update(self,idnum):
        if idnum<=newestID:
            self.mappings[idnum]
        else:
            return
    #below method is used to compare Attributes 
    #return a list of all matches
    #note that None matches all
    #and locations and sizes are not compared
    #   (rely on wide, narrow descriptors instead)
    #return list of id,Attributes pairs: [(id,Attributes)]
    def findMatches(self,attr):
        aVals = attr.values()
        matches=[]
        for (idnum,histEntry) in self.mappings.iteritems():
            if all(map(lambda x: x in aVals, entry.get().values())):
                matches.append((idnum,histEntry.get()))
        return matches


database = HistoryMap() #history of objects drawn and current objects

"""
def reprocessAttributes(attr):
    sh=canvasHeight()
    sw=canvasWidth()
    dim = attr['size']
    if dim != None:
        if dim is 'tall':

    pos = attr['positioning']
    if pos != None:
        if pos is 'top':
            attr.center=(0,sh*0.25)
"""

def drawAttributes(attr):
    sh=canvasHeight()
    shh=sh/2
    swh=canvasWidth()/2
    [cx,cy]=attr.center
    [w,h]=attr.span
    loc=[(swh+cx)-w/2,sh-((shh+cy-w/2),w,h]
    shape=attr['shape']
    color=attr['color']
    if shape is 'oval':
        attr.idnum=canvas.create_oval(loc,fill=color,tag=attr.names)
    elif shape is 'circle':
        r=(loc[2]+loc[3])/2
        attr.idnum=canvas.craete_oval([loc[0],loc[1],r,r],fill=color,tag=attr.names)
    elif shape is 'rectangle':
        attr.idnum=canvas.create_rectangle(loc,fill=color,tag=attr.names)
    elif shape is 'square':
        r=(loc[2]+loc[3])/2
        attr.idnum=canvas.create_rectangle([loc[0],loc[1],r,r],fill=color,tag=attr.names)
    elif shape is 'triangle':
        attr.idnum=canvas.create_polygon([loc[0],loc[1]+h,loc[0]+w,loc[1]+h,cx,loc[1]],fill=color,tag=attr.names)
    else:
        return
    #now our shape has been drawn, and the attribute assigned an idnum
    #this allows us to add it to the database
    global it
    global datbase
    it=database.add(attr)
    #update our canvas
    canvas.update()
    return 

def updateAttributes(attr):

"""
def undo():
    global it
    global database
    if not it is None:
        pass
"""