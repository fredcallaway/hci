from gui import *
from bash import bash

circles = []
squares = []
def draw(w, size, color, shape, loc=Point(250,250)):
	# TODO: rewrite with tkinter syntax
	width = { #this is like a switch statement
	  'small': 50
	  'big': 200
	}.get(size, 100) #100 is default
	if shape is 'circle':
		s = Circle(loc, width/2)
		circles.append(s)
	if shape is 'square':
		s = Rectangle(Point(loc.x-width/2,loc.y-width/2),
					  Point(loc.y+width/2,loc.y+width/2))
		squares.append(s)
	s.setColor(color)
	s.draw(w)

if __name__ == "__main__":
	# TODO: rewrite with tkinter syntax
    w = GraphWin("Example", 500, 500)
    e = Entry(Point(250,490),50) #input text box
    e.draw(w)
    while True: #main loop
    	if w.checkKey() == 'Return':
    		cmd = e.getText() #get input
    		print cmd
    		e.setText('')
    		if cmd == 'draw a red circle':
    			print 'drawing'
    			draw(w,'','red','circle')


def parse_cmd(cmd):
	"""translates user input into (logical notation)"""
	bash("sh ../bitpar/parse '"+cmd+"'") #ouput: [.VP [.V draw][.NP [.D a][.N-bar [.N square]]]]
	# send to lambda calculator
	# translate output into functions
	# call functions








