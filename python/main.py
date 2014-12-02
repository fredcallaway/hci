# from gui import *
from bash import bash

def AttributeList():
    #for testing purposes
    return {'shape':None,'color':None}

def parseInput(input):
    """translates user input into (logical notation)"""
    # parse=bash("sh ../bitpar/parse '"+input+"'") # ouput: [.VP [.V draw][.NP [.D a][.N-bar [.N square]]]]
    cmd="draw(Gy[red(y) & square(y)])" # send to lambda calculator
    parse(cmd)

# Gy[red(y) & square(y)]
#   - create attribute list, y
#   - go thrrough bracketed list and apply functions to y
# Gy[square(y) ] & nextTo(y,(ix[blue(x)])&square(x)]]
def parse(string):
    print "parse("+string+")"
    global local_vars # a dictionary that contains mappings from variables to attribute lists
    if string in local_vars: # e.g. 'y'
        return string 
    elif string[0]=='G':
        return G(string[1],string[3:len(string)-1])
    elif string[0]=='I':
        pass
    else:
        #interpret the argument as a string to be parsed
        fun = string.split( '(' , 1)[0] # e.g. 'draw' or 'red'
        arg = parse(string.split( '(' , 1)[1][:-1])  # e.g. 'Gy[(red(y) & square(y)]' or 'y'
        exec(fun+'(arg)')

            
#draw(Gy[(red(y) & square(y)])
def draw(attr):
    print 'Gui.create('+`local_vars[attr]`+')'
def make1(attr):
   print 'Gui.create()'

def make2(shape, attr):
    #updates shape with non-null attributes in attr
    pass

def G(var,string):
    global local_vars
    #create a new local variable
    local_vars[var]=AttributeList()
    #apply functions to new local variable, updating its attibute list
    for substring in string.split(" & "):
        parse(substring)
    return var
def I(string):
    pass

#COLORS:
def red(var):
    global local_vars
    local_vars[var]['color']='red'
def orange(var):
    global local_vars
    local_vars[var]['color']='orange'
def yellow(var):
    global local_vars
    local_vars[var]['color']='yellow'
def green(var):
    global local_vars
    local_vars[var]['color']='green'
def blue(var):
    global local_vars
    local_vars[var]['color']='blue'
def purple(var):
    global local_vars
    local_vars[var]['color']='purple'
def white(var):
    global local_vars
    local_vars[var]['color']='white'
def black(var):
    global local_vars
    local_vars[var]['color']='black'

#SHAPES:
def circle(var):
    global local_vars
    local_vars[var]['shape']='circle'
def square(var):
    global local_vars
    local_vars[var]['shape']='square'
def triangle(var):
    global local_vars
    local_vars[var]['shape']='triangle'



if __name__ == "__main__":
    local_vars={}
    parseInput("none")