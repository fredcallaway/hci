#!/usr/bin/python

from Tkinter import *
from bash import bash
from window_management import MainFrame
from parsing import runMainParser


# Some local variables
tkWindow = None
main_frame = None # container for window widgets (canvas, entry, text)
#the below may belong in another module
cmd_history = []
lambda_output_history = []




#below callback functions define workflow of window updating
#cmd line is the most important one

#TODO: define commands that short-circuit parsing, like "Undo"

def cmdLineCallback(event):
	cmd = main_frame.entry.get()
	main_frame.entry.delete(0,END)
	# command is now stored as string cmd
	if(len(str)==0):
		return
	else:
		# save it to the text box
		main_frame.text.insert(END,'> '+cmd+'\n','usr')
		cmd_history.append(cmd)
		"""
		parse=bash("sh ../bitpar/parse '"+cmd+"'") 
		# ouput: [.VP [.V draw][.NP [.D a][.N-bar [.N square]]]]
	    bash("java -jar ../lambda/lambda-auto.jar ../lambda/input.txt > ../lambda/input.tex")
	    fml=bash("make -C ../lambda input.fml")
	    print fml
	    lambdaCalc_output=`fml`.split('true ')[1]
	    lambda_output_history.append(lambdaCalc_output)
	    runMainParser(lambdaCalc_output) 
	    """



def setupWindow():
	tkWindow = Tk()
	tkWindow.title('Natural Language Drawing Application')
	main_frame=MainFrame(tkWindow)
	#main_frame now holds widgets for Canvas, Entry (aka cmd line), and Text (display)

	main_frame.focus_set()
	main_frame.entry.focus_set() #set the focus to always be on the cmd line

	#assign callback functions
	main_frame.bind('<Return>',cmdLineCallback)
	#other callback functions will be for buttons and stuff not yet implemented





def main():
	
	setupWindow() #initializes tkWindow and main_frame

	tkWindow.mainloop()


if __name__ == '__main__':
    main()  