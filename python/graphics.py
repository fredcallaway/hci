#!/usr/bin/python

from Tkinter import *
from copy import deepcopy

#reference to the graphics canvas
canvas = None
def canvasHeight():
    global canvas
    return canvas.winfo_height()
#TODO check this works
def canvasWidth():
    global canvas
    return canvas.winfo_width()
##TODO check this works
def standardSizes():
    return [100.0,100.0]

class Attributes(dict):
    # FRED: i realized that this name is very unintuitive. i think we should
    #       change it to simply Shape. that's what this object really is
    def __init__(self,*args,**kw):
        super(Attributes,self).__init__(*args,**kw)
        #define special fields
        self.center=[0.0,0.0]
        self.span=standardSizes()
        self.idnum=None # tells us if the object has been drawn

        self.names=[]
        #FRED: - an object should only be allowed to have one name, shouldn't it?
        #      - we should also prevent the user from assigning one name to two objects
        #      - rather than viewing names as an attribute of an Attributes object, we
        #        could make names a dict from names to Attributes object.
        #      - we should think of ids in the same way, but use a list; and ids are
        #        mandatory. this is what database.mappings is correct?
        #      - what if we just kept a list of shapes as they are created, then the
        #        idnum is simply the index in that list. a dictionary is just cruft


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

class HistoryEntry:
    def __init__(self,attr):
        self.history = [deepcopy(attr)]
        self.current = 0
        self.total = 1
        self.deleted = False
    def update(self,attr):
        self.history.append(deepcopy(attr))
        self.current += 1
        self.total = self.current+1 #erase Redos
    def undo(self):
        self.current -= 1
        if self.current < 0:
            self.deleted = True
            self.current = 0
            return None
        return self.get()
    def redo(self):
        self.deleted = False
        self.current += 1
        if self.current >= self.total:
            self.current = self.total-1
            return None
        return self.get()
    def get(self):
        return self.history[self.current]

class HistoryMap(dict):
    def __init__(self,*args,**kw):
        super(HistoryMap,self).__init__(*args,**kw)
        #define special fields
        self.newestID = -1
    def getNewID(self):
        self.newestID += 1
        return self.newestID
    def add(self,attr):
        #entry = self.mappings.get(attr.idnum,None)
        #if entry == None:
        self[self.getNewID()]=HistoryEntry(attr)
        #else:
        #    entry.update(attr)
        return self.newestID
    def update(self,idnum,attr):
        if idnum<=self.newestID:
            self[idnum].update(attr)
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
        for (idnum,histEntry) in self.iteritems():
            entryVals=histEntry.get().values()
            if all(map(lambda x: x is None or x in entryVals, aVals)):
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
    hsh=sh/2
    hsw=canvasWidth()/2
    [cx,cy]=attr.center
    [w,h]=attr.span
    bbox=[hsw+cx-w/2,sh-(hsh+cy-h/2),hsw+cx+w/2,sh-(hsh+cy+h/2)]
    shape=attr['shape']
    color=attr['color']
    if color is None:
        color='gray'
    if shape is 'oval':
        attr.idnum=canvas.create_oval(bbox,fill=color,tag=attr.names)
    elif shape is 'circle':
        r=(w+h)/2
        attr.idnum=canvas.craete_oval([bbox[0],bbox[1],bbox[0]+r,bbox[1]+r],fill=color,tag=attr.names)
    elif shape is 'rectangle':
        attr.idnum=canvas.create_rectangle(bbox,fill=color,tag=attr.names)
    elif shape is 'square':
        r=(bbox[2]+bbox[3])/2
        attr.idnum=canvas.create_rectangle([bbox[0],bbox[1],bbox[0]+r,bbox[1]+r],fill=color,tag=attr.names)
    elif shape is 'triangle':
        attr.idnum=canvas.create_polygon([bbox[0],bbox[3],bbox[2],bbox[3],hsw+cx,bbox[1]],fill=color,tag=attr.names)
    else:
        return
    #now our shape has been drawn, and the attribute assigned an idnum
    #update our canvas
    canvas.update()

#returns id of created history mapping
def createDrawnAttributes(attr):
    global it,datbase
    drawAttributes(attr)
    #this allows us to add it to the database
    it=database.add(attr)
    return it

#note that these dont call update on canvas
def hide(attrId):
    global database,canvas
    canvas.itemconfig(database[attrId].get().idnum, state=HIDDEN)
def unhide(attrId):
    global database,canvas
    canvas.itemconfig(database[attrId].get().idnum, state=NORMAL)

#updates Attributes with attrId
#   to Attributes in attr
def updateDrawnAttributes(attrId, attr):
    global database
    hide(attrId) #erases the previous image
    drawAttributes(attr)
    database.update(attrId,attr)
    it=attrId
    return it

def undo(attrId=None):
    global database,canvas,it
    if attrId is None and not it is None:
        attrId=it
    if not attrId is None:
        hide(attrId)
        prev = database[attrId].undo()
        if not prev is None:
            if not database[attrId].deleted:
                unhide(attrId)
                #drawAttributes(prev)
        canvas.update()

def redo(attrId=None):
    global database,canvas,it
    if attrId is None and not it is None:
        attrId=it
    if not attrId is None:
        entry = database[attrId]
        if entry.deleted:
            unhide(attrId)
        else:
            hide(attrId)
            entry.redo()
            unhide(attrId)
        canvas.update()
        

