#!/usr/bin/python

from Tkinter import *
from copy import deepcopy

#reference to the graphics canvas
canvas = None
def canvasHeight():
    global canvas
    return canvas.winfo_height()
def canvasWidth():
    global canvas
    return canvas.winfo_width()
def standardSizes():
    return [100.0,100.0]

        
class Shape(dict):
    # FRED: i realized that this name is very unintuitive. i have
    #       changed it to Shape, which is what this object really is
    def __init__(self,*args,**kw):
        super(Shape,self).__init__(*args,**kw)
        #define special fields
        self.center=(0.0,0.0)
        self.span=standardSizes()
        self.idnum=None # tells us if the object has been drawn
        self.isSet=False # object represents the set of all objects matching attrbutes
        self.name=None
        #FRED: - an object should only be allowed to have one name, shouldn't it?
        #      - we should also prevent the user from assigning one name to two objects
        #      - rather than viewing names as an attribute of an Attributes object, we
        #        should make names a dict from names to Shape object.


def relMove(shape,command):
    [x,y]=shape.center
    dh=canvasHeight() * 0.2
    dw=canvasWidth() * 0.2
    if command is 'up':
        shape.center=[x,y+dh]
    elif command is 'down':
        shape.center=[x,y-dh]
    elif command is 'left':
        shape.center=[x-dw,y]
    elif command is 'right':
        shape.center=[x+dw,y]
    else:
        return

def relSize(shape,command):
    [w,h] = shape.span
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
    shape.span=[w,h]

names={} # names to idnums
def addName(idnum,name):
    database.mappings[idnum].name=name
    names[name]=idnum

#constants for specifying attributes that are absolute, ie enumerated
attrTypes = ('kind','size','positioning')
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
def updateAttributes(shape,command):
    #check for relative changes
    for i in range(len(changeTypes)):
        if command in changeNames[i]:
            changeTypes[i](shape,command)
            return
    #check for absolute changes
    setAttributes(shape, command)

#use this function when creating a new Attributes
#ie make1
def setAttributes(shape, command):
    for i in range(len(attrTypes)):
        if command in attrNames[i]:
            shape[attrTypes[i]]=command
            return
    #if the change name is not recognized, assume it's a color
    #this way we don't have to list every single color possible
    shape['color']=command


it = None

class HistoryEntry:
    def __init__(self,shape):
        self.history = [deepcopy(shape)]
        self.current = 0
        self.total = 1
        self.deleted = False
    def update(self,shape):
        self.history.append(deepcopy(shape))
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
    def add(self,shape):
        #entry = self.mappings.get(shape.idnum,None)
        #if entry == None:
        self[self.getNewID()]=HistoryEntry(shape)
        #else:
        #    entry.update(shape)
        return self.newestID
    def update(self,idnum,shape):
        if idnum<=self.newestID:
            self[idnum].update(shape)
        else:
            return
    #below method is used to compare Shape 
    #return a list of all matches
    #note that None matches all
    #and locations and sizes are not compared
    #   (rely on wide, narrow descriptors instead)
    #return list of ids
    def findMatches(self,shape):
        aVals = shape.values()
        matches=[]
        for (idnum,histEntry) in self.iteritems():
            entryVals=histEntry.get().values()
            if all(map(lambda x: x is None or x in entryVals, aVals)):
                matches.append((idnum,histEntry.get()))
        return matches


database = HistoryMap() #history of objects drawn and current objects

"""
def reprocessAttributes(shape):
    sh=canvasHeight()
    sw=canvasWidth()
    dim = shape['size']
    if dim != None:
        if dim is 'tall':

    pos = shape['positioning']
    if pos != None:
        if pos is 'top':
            shape.center=(0,sh*0.25)
"""
def drawAttributes(shape):
    drawShape(shape)

def drawShape(shape):
    sh=canvasHeight()
    hsh=sh/2
    hsw=canvasWidth()/2
    [cx,cy]=shape.center
    [w,h]=shape.span
    bbox=[hsw+cx-w/2,sh-(hsh+cy-h/2),hsw+cx+w/2,sh-(hsh+cy+h/2)]
    kind=shape['shape']
    color=shape['color']
    if color is None:
        color='gray'
    if shape is 'oval':
        shape.idnum=canvas.create_oval(bbox,fill=color,tag=shape.names)
    elif shape is 'circle':
        r=(w+h)/2
        shape.idnum=canvas.craete_oval([bbox[0],bbox[1],bbox[0]+r,bbox[1]+r],fill=color,tag=shape.names)
    elif shape is 'rectangle':
        shape.idnum=canvas.create_rectangle(bbox,fill=color,tag=shape.names)
    elif shape is 'square':
        r=(bbox[2]+bbox[3])/2
        shape.idnum=canvas.create_rectangle([bbox[0],bbox[1],bbox[0]+r,bbox[1]+r],fill=color,tag=shape.names)
    elif shape is 'triangle':
        shape.idnum=canvas.create_polygon([bbox[0],bbox[3],bbox[2],bbox[3],hsw+cx,bbox[1]],fill=color,tag=shape.names)
    else:
        return
    #now our shape has been drawn and assigned an idnum
    #update our canvas
    canvas.update()

#returns id of created history mapping
def createDrawnAttributes(shape):
    global it,datbase
    drawAttributes(shape)
    #this allows us to add it to the database
    it=database.add(shape)
    return it

#note that these dont call update on canvas
def hide(shapeID):
    global database,canvas
    canvas.itemconfig(database[shapeID].get().idnum, state=HIDDEN)
def unhide(shapeID):
    global database,canvas
    canvas.itemconfig(database[shapeID].get().idnum, state=NORMAL)


# attaches shape to idnum
def updateDrawnShape(idnum, shape):
    global database
    hide(idnum) #erases the previous image
    drawShape(shape)
    database.update(idnum)

def undo(shapeID=None):
    global database,canvas,it
    if shapeID is None and not it is None:
        shapeID=it
    if not shapeID is None:
        hide(shapeID)
        prev = database[shapeID].undo()
        if not prev is None:
            if not database[shapeID].deleted:
                unhide(shapeID)
                #drawAttributes(prev)
        canvas.update()

def redo(shapeID=None):
    global database,canvas,it
    if shapeID is None and not it is None:
        shapeID=it
    if not shapeID is None:
        entry = database[shapeID]
        if entry.deleted:
            unhide(idnum)
        else:
            hide(idnum)
            entry.redo()
            unhide(shapeID)
        canvas.update()
