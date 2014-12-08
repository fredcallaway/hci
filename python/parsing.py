#!/usr/bin/python

#This module contains the parsing functions
# from Lambda Calculator to graphics calls
# It imports attribute lists and graphics objects
# used by graphics

import graphics
from bash import bash
import re
shapes = graphics.database.mappings
references = graphics.database.references
local_vars = {}
class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def runMainParser(cmd):
    global local_vars
    local_vars={}
    """translates user input into logical notation
        - parse works recursively, applying functions and operators
        - variables in logical notation are stored in local_vars
            - these variables are tied to an Attributes object
    """
    # bitpar
    cmd=clean(cmd)
    cmd=str(bash("sh ../bitpar/parse '"+cmd+"'"))
    cmd=label(cmd)

    # update input.txt
    bash("cp ../lambda/lambda-defs.txt ../lambda/input.txt")
    bash("echo '"+cmd+"' >> ../lambda/input.txt")

    # lambda calculator & plop
    bash("java -jar ../lambda/lambda-auto.jar ../lambda/input.txt > ../lambda/input.tex")
    bash("make -C ../lambda input.fml")
    fml=`bash('cat ../lambda/input.fml')`
    if fml == '': raise ParseError('cannot be interpreted by lambda calculator')
    lambdaCalc_output=fml.split('true ')[1][:-1]
    #lambda_output_history.append(lambdaCalc_output) #out of scope. how do i fix this?
    print lambdaCalc_output
    parse(lambdaCalc_output)

def clean(cmd):
    cmd = re.sub('next to', 'next-to', cmd)
    cmd = re.sub('on top of', 'on-top-of', cmd)
    return cmd

def label(cmd):
    # see lambda-defs.txt for explanation of labels
    cmd = cmd.replace('make][.NP', 'make1][.NP')
    cmd = cmd.replace('make][.SC', 'make2][.SC')
    cmd = re.sub('(draw.*)one','\\1one1',cmd)
    cmd = re.sub('(make1.*)one','\\1one1',cmd)
    cmd = re.sub('(make2.*)one','\\1one2',cmd)
    cmd = '[result ' + cmd + ']' #dummy function for plop
    return cmd


def parse(string):
    global local_vars
    # print "parse("+string+")"

    # variables
    if string in local_vars: # e.g. 'y'
        return string
        print string
    elif string in graphics.names:
        return graphics.names[string]
    elif string == 'it':
        # print 'it: ',references[0]
        return references[0]

    # operators
    elif string.find('\gamma') == 0:
        return gamma(string[7],string[9:-1])
    elif string.find('\iota') == 0:
        # treating iota as gamma for now
        return gamma(string[6],string[8:-1])

    # function application
    else:
        fun = string.split( '(' , 1)[0]
        arg = parse(string.split( '(' , 1)[1][:-1])
        exec(fun+'(arg)')


def draw(var):
    """draws the hypothetical shape associated with var"""
    shape=getShape(var)
    graphics.createShape(shape)

def hide(id):
    """hides the existing shape associated with id"""
    shape = getShape(id)
    if shape.idnum: # id refers to an existing shape
        graphics.hide(shape)
    else: # id refers to hypothetical shape
        graphics.hide(pick(shape))
        # TODO: implement pick()
    
def itParamaters(id):
    """fills unspecified attributes of var with attributes of references[0]"""
    shape=getShape(id)
    it = getShape(references[0])
    for attribute in it:
            graphics.updateAttributes(shape, it[attribute])

def one2(id):
    """returns: most recently mentioned shape with properties in shape"""
    shape=getShape(id)
    pass


#OPERATORS:
def gamma(var, string):
    """returns: var tied to a new shape with attributes described in string"""
    global local_vars
    #create a new local variable
    local_vars[var]=graphics.Shape()
    #apply functions to new local variable, updating its attibute list
    for substring in string.split(" & "):
        parse(substring)
    return var

def iota(var, string):
    """returns: idnum of the unique shape matching attributes in string
       throw error: "iota ambiguity" if there is not a unique shape"""
    global local_vars
    local_vars[var]=graphics.Attributes()
    for substring in string.split(" & "):
        parse(substring)
    matches = graphics.findMatches(local_vars[var])
    if len(matches) != 1: raise ParseError('iota ambiguity')
    idnum = matches[0][0]
    return idnum

#COLORS:
def red(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'red')
def orange(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'orange')
def yellow(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'yellow')
def green(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'green')
def blue(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'blue')
def purple(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'purple')
def white(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'white')
def black(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'black')

#SIZES:
def tall(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'tall')
def short(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'short')
def wide(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'wide')
def narrow(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'narrow')
def large(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'large')
def small(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'small')

#LOCATIONS:
def left(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'left')
def right(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'right')
def up(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'up')
def down(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'down')

def leftOf(id1,id2):
    shape1=getShape(id1)
    shape2=getShape(id2)
    # uncertain values are functions that return True if given a value that matches the requirement
    # TODO: combine functions for "to the left of the triangle and above the square"
    loc= lambda (x,y): x < shape2['center'] - (shape2['span'][0]/2 + shape1['span'][0]/2)
def rightOf(id1,id2):
    shape1=getShape(id1)
    shape2=getShape(id2)
    loc= lambda (x,y): x > shape2['center'] + (shape2['span'][0]/2 + shape1['span'][0]/2)
def below(id1,id2):
    shape1=getShape(id1)
    shape2=getShape(id2)
    loc= lambda (x,y): x < shape2['center'] - (shape2['span'][1]/2 + shape1['span'][1]/2)
def above(id1,id2):
    shape1=getShape(id1)
    shape2=getShape(id2)
    loc= lambda (x,y): y > shape2['center'] + (shape2['span'][1]/2 + shape1['span'][1]/2)
def over(id1,id2):
    pass
def inside(id1,id2):
    pass

#KINDS:
def circle(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'circle')
def square(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'square')
def triangle(id):
    shape=getShape(id)
    graphics.updateAttributes(shape, 'triangle')
    

#HELPERS:
def getShape(id):
    if type(id)==int: # idnum
        return shapes[id]
    elif type(id)==str and len(id)==1: # local var
        return local_vars[id]
    else: # name
        return shapes[graphics.names[id]]


if __name__ == "__main__":
    # parse("draw(\gamma y(large(y) & square(y))).")
    # runMainParser("make a red triangle")
    # runMainParser("put the square next to the circle")
    runMainParser("make the red triangle")
    runMainParser("delete the triangle")