from graphics import *

# n_ircles = 0
# n_square = 0
circles = []
squares = []
def draw(w, size, color, shape, loc=Point(250,250)):
	width = { #this is like a switch statement
	  'small': 50,
	  'big': 200
	}.get(size, 100) #100 is default
	if shape is 'circle':
		# n_circles += 1
		s = Circle(loc, width/2)
		circles.append(s)
	if shape is 'square':
		s = Rectangle(Point(loc.x-width/2,loc.y-width/2),
					  Point(loc.y+width/2,loc.y+width/2))
		squares.append(s)
	s.setColor(color)
	s.draw(w)

if __name__ == "__main__":
    w = GraphWin("Example", 500, 500)
    e = Entry(Point(250,490),50)
    e.draw(w)
    while True: #main loop
    	if w.checkKey() == 'Return':
    		cmd = e.getText()
    		print cmd
    		e.setText('')
    		if cmd == 'draw a red circle':
    			print 'drawing'
    			draw(w,'','red','circle')

# to implement:

# def parse_cmd(cmd):
# 	"""translates user input into (logical notation)"""









