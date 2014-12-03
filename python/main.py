# from gui import *
from bash import bash

def AttributeList():
    #for testing purposes
    return {'shape':None,'color':None}

def parseInput(input):
    """translates user input into (logical notation)
        - parse works recursively, applying functions and operators
        - variables in logical form are stored in local_vars
            - these variables are tied to an attribute list
            - a variable can represent an existing shape or a hypothetical shape
    """
    # parse=bash("sh ../bitpar/parse '"+input+"'") # ouput: [.VP [.V draw][.NP [.D a][.N-bar [.N square]]]]
    bash("java -jar ../lambda/lambda-auto.jar ../lambda/input.txt > ../lambda/input.tex")
    fml=bash("make -C ../lambda input.fml")
    print fml
    cmd=`fml`.split('true ')[1]
    
    # TEST CASES
    # cmd="draw(Gy[red(y) & square(y)])" 
    cmd="draw(\gamma y(red(y) & square(y)))."

    print cmd
    parse(cmd)
#   - create attribute list, y
#   - go thrrough bracketed list and apply functions to y
# Gy[square(y) ] & nextTo(y,(ix[blue(x)])&square(x)]]
def parse(string):
    print "parse("+string+")"
    global local_vars # a dictionary that contains mappings from variables to attribute lists
    if string in local_vars: # e.g. 'y'
        return string 
    # if string in names:
        # return string

    # operators
    elif string.find('\gamma') == 0:
        return gamma(string[7],string[9:len(string)-2])
    elif string.find('\iota') == 0:
        # treating iota as gamma for now
        return gamma(string[7],string[9:len(string)-2])

    else: # function application
        fun = string.split( '(' , 1)[0] # e.g. 'draw' or 'red'
        arg = parse(string.split( '(' , 1)[1][:-1])  # e.g. 'Gy[(red(y) & square(y)]' or 'y'
        exec(fun+'(arg)')

def draw(attr):
    print 'Gui.create('+`local_vars[attr]`+')'
def make1(attr):
   print 'Gui.create()'

def make2(shape, string):
    # updates shape with non-null attributes in attr
    pass

def gamma(var,string):
    # returns variable associated with attribute list from attributes in string
    global local_vars
    #create a new local variable
    local_vars[var]=AttributeList()
    #apply functions to new local variable, updating its attibute list
    for substring in string.split(" & "):
        parse(substring)
    return var

# NIKITA
def iota(var, string):
    # goes through existing shapes and finds ones that matches attributes in string
    # if there is one shape that matches, assign var to that shape
    # else, throw error: "iota ambiguity"

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