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





#Below code defines various standard sizes and positioning quantities
#The idea was to add user feedback, and change these models based on it

def standardSizes():
    return [100.0,100.0]

#below models are for lateral/vertical movement
def verticalModel():
    h=canvasHeight()
    return [h/2,-h/2]
def horizontalModel():
    w=canvasWidth()
    return [w/2,-w/2]

#below models are for resizing
def largeModel():
    [w,h]=standardSizes()
    return [w*3,h*3]
def smallModel():
    [w,h]=standardSizes()
    return [w/3,h/3]

#below model is for relative positioning. Uses a uniform random distribution to spice things up :)
def proximityModel(centerDforAdjacent):
    return centerDforAdjacent*(1+0.8*rand.random())





#The bread and butter of image descriptions. 
#Contains positioning information, information for finding the image on the Canvas (imageID and names)
#The class is also a Dicionary, allowing us to map arbitrary values to attributes
#indexing into an AttributeList like into a dictionary, with the string name of the attribute in question. 
#Usage: attList['attribute_name'] = attribute_value
class AttributeList(dict):
    def __init__(self,*args,**kw):
        super(AttributeList,self).__init__(*args,**kw)
        #define special fields
        self.center=(0.0,0.0)
        self.span=standardSizes()
        self.imageID=None # tells us if the object has been drawn
        #   imageID corresponds with the id of a Tkinter Canvas-based image
        #   which is the most basic level of the structure
        self.names=[]






## The below functions change attributes that are stored in the attList's dictionary. 
## These correlate directly to the enumerated attributes at the top of this file. 

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

# List of functioins that handle changing enumerated attributes 
attrHandlers = (kindHandler,sizeHandler,positioningHandler,colorHandler)





##  The below functions are designed to update attList, to be called by the main
##  updateAttList() function, or the updateAttList2() function (when the change is 
##  in relation to another attList)

#Changes the attribute's spatial descriptors. 
#Updates the attList
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

# List of functions that handle changing an AttList
# grouped by keywords in the changeNames list lists
changeHandlers = (relMove, relSize)





## Below functions handle changes to the first attList 
## when the changes are in realtion to the second attList2

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

#list of above functions, grouped by keywords
relativeHandlers = (relativePositioningHandler)



## The setAttList(), updateAttList(), and updateAttList2() functions operate on
## the first AttributeList given to them, interpreting a particular command
## the functions differ based on which set of attribute or change names they search
## through. Note that attrNames, changeNames, and relativeNames are grouped into lists
## of lists. The index of the name group in which the command is found is used to
## to index into the appropriate handler


#use this function when creating a new Attributes
#ie make1
def setAttList(attList, command):
    for i in range(len(attrTypes)):
        if command in attrNames[i]:
            attrHandlers[i](attList,command)

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


def updateAttList2(attList,attList2,command):
    for i in range(len(relativeNames)):
        if command in relativeNames[i]:
            relativeHandlers[i](attList,attList2,command)
    






##### -------------------------------------------------------------------
##### Code below is used for attributes linked to a physical 
##### representation on the screen 
##### -------------------------------------------------------------------


# shapeID reference to the latest Shape edited
it = None


#This class defines a history of images. This is what we consider a shape
#each image has an AttributeList associated with it to describe it
#The Shape supports undo and redo thanks to this structure, as well 
# as arbitrary changes. 

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
    #returns the descriptor of the current image's attributes
    def getAttList(self):
        return self.history[self.current]


#Each Shape is given a shapeID
#The shapeID maps to a Shape object in HistoryMap
#The history map allows the creation of new Shapes
# and the update of old ones
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
            for (key,val) in attList.iteritems():
                if key in attrTypes:
                    if not val in shapeVals:
                        matchesThisShape = False
                #elif key in 
            if matchesThisShape:
                matches.append(shapeID)
        return matches

#contains the order of shapeID creations/updates
#simply a list of shapeID's with some reverse searching functionality
# future plans for this class included adding timestamps to each change
# which would've allowed us to group objects based on references such as "them"
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




### Below are the objects that keep track of our shapes 

database = HistoryMap()  # mapping of shapeID's to all current drawn images on Canvas

referenceOrder = DrawOrder()  # self-explanatory -- order of shapeID modifications

### 




#The below function is very low-level. It converts from attribute list to a tkinter shape, and updates the canvas. Other functions use this to encapsulate drawing

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




#The below function is what is actually used by parsing to draw things on screen
#Creates a new shape in the databas, drawing the given AttributeList
#returns id of created history mapping
def createShape(attList):
    global it,datbase
    drawAttList(attList)
    #this allows us to add it to the database
    it=database.add(attList)
    global referenceOrder
    referenceOrder.add(it)
    return it

#The below function is what is actually used by parsing to draw things on screen
# Hides the shapeID's Shape old image, and  draws the given AttributeList
# attaches AttributeList to Shape history in the database
def updateShape(shapeID, attList):
    global database
    hide(shapeID) #erases the previous image
    drawAttList(attList)
    database.update(shapeID,attList)
    global referenceOrder
    referenceOrder.add(shapeID)



### Helper functions for drawing
# The below functions are mainly used by graphics
# Shape update is base on hiding an old image, and drawing a new one
# Undos and Redos are based on the same
# These functions allow a direct interface with Tkinter through information stored for a Shape in the database



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