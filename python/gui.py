#!/usr/bin/python
"""Gui is a Tkinter Entry object cmd line interface coupled with a Tkinter Canvas object 
for display and Text object for history. The cmd line accepts natural language input
and the Canvas serves as the graphical interface. """

from Tkinter import *

"""
class ObjInfo:
	def __init__(self, id, name, color, width, height):
		self.id = id
		self.name = name
		self.color = color
		self.width = width
		self.height = height
"""

class Gui:
	def __init__(self, width=400, height=400):
		self.canvasWidth = width
		self.canvasHeight = height
		self.Wcenter = self.canvasWidth/2
		self.Hcenter = self.canvasHeight/2
		self.window = Tk()
		self.canvas = Canvas(self.window, width = self.canvasWidth, height = self.canvasHeight) #canvas widget
		self.canvas.pack() #arranges window components in a certain way. Alternatively, can use grid
		self.objectList = []

	def oval(self,name,color="cyan",Xdiam=120,Ydiam=80):
		halfX=Xdiam/2
		halfY=Ydiam/2
		ovalId = self.canvas.create_oval(self.Wcenter-halfX,self.Hcenter-halfY,self.Wcenter+halfX,self.Hcenter+halfY,fill=color,tag=name)
		self.objectList.append(ovalId)
		self.canvas.update()
	def circle(self, name, color="green", diameter=80):
		radius = diameter/2
		circleId = self.canvas.create_oval(self.Wcenter - radius, self.Hcenter - radius, self.Wcenter+ radius, self.Hcenter + radius, fill=color, tag=name)
		self.objectList.append(circleId)
		self.canvas.update()
	def rectangle(self,name,color="orange",sideX=120,sideY=80):
		halfX=sideX/2
		halfY=sideY/2
		rectID = self.canvas.create_rectangle(self.Wcenter-halfX,self.Hcenter-halfY,self.Wcenter+halfX,self.Hcenter+halfY,fill=color,tag=name)
		self.objectList.append(rectID)
		self.canvas.update()
	def square(self, name, color="red",side=80):
		radius = side/2
		squareID = self.canvas.create_rectangle(self.Wcenter - radius, self.Hcenter - radius, self.Wcenter + radius, self.Hcenter + radius, fill=color, tag=name)
		self.objectList.append(squareID)
		self.canvas.update()

	def changeColor(self,name,color):
		self.canvas.itemconfig(name,fill=color)
		self.canvas.update()

	#positions object A next to object B, on the right by default
	def positionNextTo(self,nameA,nameB,where="right"):
		acoord = self.canvas.coords(nameA)
		bcoord = self.canvas.coords(nameB)
		wha = (acoord[2]-acoord[0])/2 #half-width
		hha = (acoord[3]-acoord[1])/2 #half-height
		wcb = (bcoord[2]-bcoord[0])/2 + bcoord[0] #center width
		hcb = (bcoord[3]-bcoord[1])/2 + bcoord[1] #center height
		if where=='right':
			self.canvas.coords(nameA,bcoord[2],hcb-hha,bcoord[2]+2*wha,hcb+hha)
		elif where=='left':
			self.canvas.coords(nameA,bcoord[0]-2*wha,hcb-hha,bcoord[0],hcb+hha)
		elif where=='below':
			self.canvas.coords(nameA,wcb-wha,bcoord[3],wcb+wha,bcoord[3]+2*hha)
		elif where=='above':
			self.canvas.coords(nameA,wcb-wha,bcoord[1]-2*hha,wcb+wha,bcoord[1])
		else:
			print "I don't know that position!"
		self.canvas.update()

	def moveExactly(self,name,dx,dy):
		coord = self.canvas.move(name,dx,dy)
		self.canvas.update()
	#for moving abstractly
	def move(self,name,dir):
		dx = self.canvasWidth*0.1
		dy = self.canvasHeight*0.1
		if dir=='right':
			self.canvas.move(name,dx,0)
		elif dir=='left':
			self.canvas.move(name,-dx,0)
		elif dir=='up':
			self.canvas.move(name,0,dy)
		elif dir=='down':
			self.canvas.move(name,0,-dy)
		else:
			print "I don't understand that direction!"

	def hide(self,name):
		self.canvas.itemconfig(name,state=HIDDEN)
		self.canvas.update()
	def unhide(self,name):
		self.canvas.itemconfig(name,state=NORMAL)
		#bring to top so the user can see it
		#self.canvas.tag_raise(name) #?? do we want to do it this way
		self.canvas.update()

	def setBackground(self,color='white'):
		self.canvas.config(background=color)
		self.canvas.update()

	def layer(self,name,upordown,of=None):
		if of==None:
			if upordown=='ab'
			self.canvas.tag_raise(name)
			self.canvas.update()
		else:
			print "I don't know how to do that yet."

