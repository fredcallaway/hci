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



# ON HOLD until we figure out how we're getting LC output
# for now, assume you have output like this:
# 
#
def parse_cmd(input):
	"""translates user input into (logical notation)"""
	parse=bash("sh ../bitpar/parse '"+input+"'") # ouput: [.VP [.V draw][.NP [.D a][.N-bar [.N square]]]]
	cmd="draw(Gy[(red(y) ∧ square(y)])" # send to lambda calculator
    

    # Gy[(red(y) ∧ square(y)]
    #   - create attribute list, y
    #   - go thrrough bracketed list and apply functions to y
    # Gy[square(y) ] ∧ nextTo(y,(ix[blue(x)])∧square(x)]]
        

def create(attr):
    pass

def change(shape, attr):
    pass

## PARSE COMMANDS

def draw(attr):
    
    #draws a shape with attributes in attr
    #adds shape to list of shapes
    pass

def make2(shape, attr):
    #updates shape with attributes in attr
    pass

def G(attr):
    #creates a shape (not draw it)
    pass

def I(attr):
    pass

# attr: property list, may contain nulls
# shape: existing object, contains a full attr (no null values)
# 


