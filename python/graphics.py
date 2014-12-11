#!/usr/bin/python

from Tkinter import *
from copy import deepcopy
import random as rand


#constants for specifying attributes that are absolute, ie enumerated
#for predicates used as shape descriptors
attrTypes = ('kind','size','positioning','color')
attrNames = (
    ('oval','circle','rectangle','square','triangle'),
    ('tall','short','wide','narrow','large','small'),
    ('screenTop','screenBottom','screenLeft','screenRight','screenCenter'),
    ('red','orange','yellow','green','blue','purple','white','black')
)
#The below lists have an associated changeHandlers and relativeHandlers lists
#    which map from the change type to a function that accepts the associated change names
#for predicates that change an attribute list but do not describe it 
changeNames = (
    ('up','down','left','right'), #movement
    ('taller','shorter','wider','narrower','larger','smaller') #size change
)
#for 2-argument predicates that change an attribute list
relativeNames = (
    ('leftOf','rightOf','over','under','nextTo','insideOf')
)

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
def verticalModel():
    h=canvasHeight()
    return [h/2,-h/2]
def horizontalModel():
    w=canvasWidth()
    return [w/2,-w/2]
def largeModel():
    [w,h]=standardSizes()
    return [w*3,h*3]
def smallModel():
    [w,h]=standardSizes()
    return [w/3,h/3]
def proximityModel(centerDforAdjacent):
    return centerDforAdjacent*(1+0.8*rand.random())

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
    elif command is 'larger': # or command is 'bigger' or command is 'enlarge':
        # the other words are mapped to 'larger' by lambda calculator
        w *= 1.3
        h *= 1.3
    elif command is 'smaller':
        w /= 1.3
        h /= 1.3
    else:
        return
    attList.span=[w,h]

"""
relationTypes = ('relPosition')
relationNames = (
    ('leftOf','')
)
"""
#constants for changing, relative absolutes
changeHandlers = (relMove, relSize)

def reprocessSizeAttributes(attList):
    [lw,lh] = largeModel()
    [sw,sh] = smallModel()
    [w,h] = attList.span


def kindHandler(attList,command):
    attList['kind']=command
def sizeHandler(attList,command):
    [w,h] = attList.span
    [lw,lh] = largeModel()
    [sw,sh] = smallModel()
    if command is None:
        return
    elif command is 'tall':
        h=lh
    elif command is 'short':
        h=sh
    elif command is 'wide':
        w = lw
    elif command is 'narrow':
        w = sw
    elif command is 'large':
        w=lw
        h=lh
    elif command is 'small':
        w=sw
        h=sh 
    attList.span=[w,h]
def positioningHandler(attList,command):
    [x,y]=attList.center
    [ty,by]=verticalModel()
    [lx,rx]=horizontalModel()
    if command is None:
        return
    elif command is 'screenTop':
        y=ty
    elif command is 'screenBottom':
        y=by
    elif command is 'screenLeft':
        x=lx
    elif command is 'screenRight':
        x=rh
    elif command is 'screenCenter':
        [x,y]=[0,0]
    attList.center=[x,y]
def colorHandler(attList,command):
    attList['color']=command
attrHandlers = (kindHandler,sizeHandler,positioningHandler,colorHandler)

#use this when updating Attributes
#ie make2
def updateAttList(attList,command):
    #check for relative changes
    for i in range(len(changeNames)):
        if command in changeNames[i]:
            changeHandlers[i](attList,command)
            return
    #check for absolute changes
    setAttList(attList, command)

def relativePositioningHandler(attList,attList2,command):
    [x,y]=attList.center
    [x2,y2]=attList2.center
    [w,h]=attList.span
    [w2,h2]=attList2.span
    if command is None:
        return
    elif command is 'leftOf':
        d=proximityModel((w+w2)/2)
        x=x2-d
    elif command is 'rightOf' or command is 'nextTo':
        d=proximityModel((w+w2)/2)
        x=x2+d
    elif command is 'over':
        d=proximityModel((h+h2)/2)
        y=y2+d
    elif command is 'under':
        d=proximityModel((h+h2)/2)
        y=y2-d
    elif command is 'insideOf':
        #TODO make this re-layer attList over attList2!!
        [x,y]=[x2,y2]
    attList.center=[x,y]
relativeHandlers = (relativePositioningHandler)

def updateAttList2(attList,attList2,command):
    for i in range(len(relativeNames)):
        if command in relativeNames[i]:
            relativeHandlers[i](attList,attList2,command)
    




#use this function when creating a new Attributes
#ie make1
def setAttList(attList, command):
    for i in range(len(attrTypes)):
        if command in attrNames[i]:
            attrHandlers[i](attList,command)


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
            matchesThisShape=True
            for (key,val) in attList:
                if key in attrTypes:
                    if not val in shapeVals:
                        matchesThisShape = False
                #elif key in 
            if matchesThisShape:
                matches.append(shapeID)
        return matches

#contains the order of shapeID creations/updates
class DrawOrder():
    def __init__(self):
        self.order=[]
    #takes a shapeID
    #update by adding a shapeID of the latest shape drawn
    def add(self,shapeID):
        self.order.append(shapeID)
    # returns the latest shapeID in the list
    def it(self):
        if len(self.order)>0:
            return self.order[len(self.order)-1]
        else:
            return None
    #takes a list shapeIDs
    #returns the latest shapeID in the order that is also in shapeIDs
    def pickMostRecent(self,shapeIDList):
        l = len(self.order)
        i=l-1
        while i>=0:
            if self.order[i] in shapeIDList:
                return self.order[i]
            i-=1
        return None


database = HistoryMap() #history of objects drawn and current objects

referenceOrder = DrawOrder()


def drawAttList(attList):
    sh=canvasHeight()
    hsh=sh/2
    hsw=canvasWidth()/2
    [cx,cy]=attList.center
    [w,h]=attList.span
    bbox=[hsw+cx-w/2,sh-(hsh+cy-h/2),hsw+cx+w/2,sh-(hsh+cy+h/2)]
    shape=attList['kind']
    color=attList.get('color')
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
        r=(w+h)/2
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
    global referenceOrder
    referenceOrder.add(it)
    return it
# attaches attList to shapeID history, draws new shape
def updateShape(shapeID, attList):
    global database
    hide(shapeID) #erases the previous image
    drawAttList(attList)
    database.update(shapeID,attList)
    global referenceOrder
    referenceOrder.add(shapeID)

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

#returns the attribute list of it
def getIt():
    global database,it
    return database[it].getAttList()