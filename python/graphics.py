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

        
class AttributeList(dict):
    def __init__(self,*args,**kw):
        super(AttributeList,self).__init__(*args,**kw)
        #define special fields
        self.center=(0.0,0.0)
        self.span=standardSizes()
        self.imageID=None # tells us if the object has been drawn
        self.names=[]


def relMove(attList,command):
    [x,y]=attList.center
    dh=canvasHeight() * 0.2
    dw=canvasWidth() * 0.2
    if command is 'up':
        attList.center=[x,y+dh]
    elif command is 'down':
        attList.center=[x,y-dh]
    elif command is 'left':
        attList.center=[x-dw,y]
    elif command is 'right':
        attList.center=[x+dw,y]
    else:
        return

def relSize(attList,command):
    [w,h] = attList.span
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
    attList.span=[w,h]

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
relationTypes = ('relPosition')
relationNames = (
    ('left','')
)

#use this when updating Attributes
#ie make2
def updateAttList(attList,command):
    #check for relative changes
    for i in range(len(changeTypes)):
        if command in changeNames[i]:
            changeTypes[i](attList,command)
            return
    #check for absolute changes
    setAttList(attList, command)

#use this function when creating a new Attributes
#ie make1
def setAttList(attList, command):
    for i in range(len(attrTypes)):
        if command in attrNames[i]:
            attList[attrTypes[i]]=command
            return
    #if the change name is not recognized, assume it's a color
    #this way we don't have to list every single color possible
    attList['color']=command


it = None

class Shape:
    def __init__(self,attList):
        self.history = [deepcopy(attList)]
        self.current = 0
        self.total = 1
        self.deleted = False
    def update(self,attList):
        self.history.append(deepcopy(attList))
        self.current += 1
        self.total = self.current+1 #erase Redos
    def undo(self):
        self.current -= 1
        if self.current < 0:
            self.deleted = True
            self.current = 0
            return None
        return self.getAttList()
    def redo(self):
        self.deleted = False
        self.current += 1
        if self.current >= self.total:
            self.current = self.total-1
            return None
        return self.getAttList()
    def getAttList(self):
        return self.history[self.current]

class HistoryMap(dict):
    def __init__(self,*args,**kw):
        super(HistoryMap,self).__init__(*args,**kw)
        #define special fields
        self.newestID = -1
    def getNewID(self):
        self.newestID += 1
        return self.newestID
    def add(self,attList):
        self[self.getNewID()]=Shape(attList)
        return self.newestID
    def update(self,shapeID,attList):
        if shapeID<=self.newestID:
            self[shapeID].update(attList)
        else:
            return
    #below method is used to compare AttributeList 
    #return a list of all matches
    #note that None matches all
    #and locations and sizes are not compared
    #   (rely on wide, narrow descriptors instead)
    #return list of ids
    def findMatches(self,attList):
        searchVals = attList.values()
        matches=[]
        for (shapeID,shape) in self.iteritems():
            shapeVals=shape.getAttList().values()
            if all(map(lambda x: x is None or x in shapeVals, searchVals)):
                matches.append(shapeID)
        return matches


database = HistoryMap() #history of objects drawn and current objects

"""
def reprocessAttributes(attList):
    sh=canvasHeight()
    sw=canvasWidth()
    dim = attList['size']
    if dim != None:
        if dim is 'tall':

    pos = attList['positioning']
    if pos != None:
        if pos is 'top':
            attList.center=(0,sh*0.25)
"""
def drawAttList(attList):
    sh=canvasHeight()
    hsh=sh/2
    hsw=canvasWidth()/2
    [cx,cy]=attList.center
    [w,h]=attList.span
    bbox=[hsw+cx-w/2,sh-(hsh+cy-h/2),hsw+cx+w/2,sh-(hsh+cy+h/2)]
    shape=attList['kind']
    color=attList['color']
    if color is None:
        color='gray'
    if shape is 'oval':
        attList.imageID=canvas.create_oval(bbox,fill=color,tag=attList.names)
    elif shape is 'circle':
        r=(w+h)/2
        attList.imageID=canvas.create_oval([bbox[0],bbox[1],bbox[0]+r,bbox[1]+r],fill=color,tag=attList.names)
    elif shape is 'rectangle':
        attList.imageID=canvas.create_rectangle(bbox,fill=color,tag=attList.names)
    elif shape is 'square':
        r=(bbox[2]+bbox[3])/2
        attList.imageID=canvas.create_rectangle([bbox[0],bbox[1],bbox[0]+r,bbox[1]+r],fill=color,tag=attList.names)
    elif shape is 'triangle':
        attList.imageID=canvas.create_polygon([bbox[0],bbox[3],bbox[2],bbox[3],hsw+cx,bbox[1]],fill=color,tag=attList.names)
    else:
        return
    #now our attList has been drawn and assigned an imageID
    #update our canvas
    canvas.update()

#returns id of created history mapping
def createShape(attList):
    global it,datbase
    drawAttList(attList)
    #this allows us to add it to the database
    it=database.add(attList)
    return it
# attaches attList to shapeID history, draws new shape
def updateShape(shapeID, attList):
    global database
    hide(shapeID) #erases the previous image
    drawAttList(attList)
    database.update(shapeID,attList)

#note that these dont call update on canvas
def hide(shapeID):
    global database,canvas
    canvas.itemconfig(database[shapeID].getAttList().imageID, state=HIDDEN)
def unhide(shapeID):
    global database,canvas
    canvas.itemconfig(database[shapeID].getAttList().imageID, state=NORMAL)



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
            unhide(shapeID)
        else:
            hide(shapeID)
            entry.redo()
            unhide(shapeID)
        canvas.update()
