#!/usr/bin/python

#import graphics
from Tkinter import *
from window_management import MainFrame
from parsing import runMainParser

from common import stdoutIO

import graphics as g
gns = {}
lns = {}
ns={}
def foo():
    global alst
    alst=g.AttributeList()
    print 'alst=AttributeList()'
    g.setAttList(alst,'oval')
    g.setAttList(alst,'green')
    g.createShape(alst)
def runCodeParser(cmd):
    global ns,gns,lns
    code=compile(cmd,'<string>','exec')
    with stdoutIO() as (out):
        #ns['it']=g.it
        gns.update(globals())
        lns.update(locals())
        exec cmd in gns,lns
    out.seek(0)
    cont = out.read()
    out.close()
    lc=len(cont)
    
    # err.seek(0)
    # e=err.read()
    # err.close()
    # le=len(e)

    # if le>0 and e[le-1]=='\n':
    #     e=e[0:(le-1)]
	
    if lc>0 and cont[lc-1]=='\n':
        cont=cont[0:(lc-1)]

    if lc>0:# or le>0:
        return (cont)#,e)
    else:
        return None

# Some local variables
tkWindow = None
main_frame = None # container for window widgets (canvas, entry, text)
#the below may belong in another module
cmd_history = []
cmd_index=0
temp_cmd=""

def cmdLineHistoryDown(event):
	global main_frame,cmd_history,cmd_index,temp_cmd
	cmd_index+=1
	if cmd_index>len(cmd_history):
		cmd_index= len(cmd_history)
	elif cmd_index==len(cmd_history):
		#reload latest typed
		main_frame.entry.delete(0,END)
		main_frame.entry.insert(0,temp_cmd)
	else:
		main_frame.entry.delete(0,END)
		main_frame.entry.insert(0,cmd_history[cmd_index])


def cmdLineHistoryUp(event):
	global main_frame,cmd_history,cmd_index,temp_cmd
	if len(cmd_history) == cmd_index:
		temp_cmd = main_frame.entry.get()
	cmd_index-=1
	main_frame.entry.delete(0,END)
	if cmd_index<0:
		cmd_index= -1
		#clear cmd line
	else:
		main_frame.entry.insert(0,cmd_history[cmd_index])


#below callback functions define workflow of window updating
#cmd line is the most important one

#TODO: define commands that short-circuit parsing, like "Undo"

def cmdLineCallback(event):
	global tkWindow,main_frame
	global cmd_history,cmd_index
	cmd = main_frame.entry.get()
	main_frame.entry.delete(0,END)
	# command is now stored as string cmd
	if(len(cmd)==0):
		return
	else:
		# save it to the text box
		main_frame.text.insert(END,'> '+cmd+'\n','usr')
		cmd_history.append(cmd)
		cmd_index = len(cmd_history)
		#-----
		#Run the Parser
		response=runMainParser(cmd)
		#response=runCodeParser(cmd)
		#-----
		#Handle output
		if not response is None:
			(out)=response
			if not (out is None):
				main_frame.text.insert(END,'< '+out+'\n','app')
			
			# if not (err is None or len(err)==0):
			# 	main_frame.text.insert(END,'x '+err+'\n','err')
		try:
			main_frame.text.see("end")
		except:
			main_frame.text.yview_pickplace("end")
		main_frame.text.update()

def setupWindow():
	global tkWindow,main_frame
	tkWindow = Tk()
	tkWindow.title('Natural Language Drawing Application')
	main_frame=MainFrame(tkWindow)
	#main_frame now holds widgets for Canvas, Entry (aka cmd line), and Text (display)
	g.canvas=main_frame.canvas

	main_frame.focus_set()
	main_frame.entry.focus_set() #set the focus to always be on the cmd line

	#assign callback functions
	main_frame.entry.bind('<Return>',cmdLineCallback)
	main_frame.entry.bind('<Up>',cmdLineHistoryUp)
	main_frame.entry.bind('<Down>',cmdLineHistoryDown)
	#other callback functions will be for buttons and stuff not yet implemented

def main():
	global tkWindow
	setupWindow() #initializes tkWindow and main_frame
	tkWindow.mainloop()


if __name__ == '__main__':
    main()  