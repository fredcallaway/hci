#!/usr/bin/python

#This module contains the parsing functions
# from Lambda Calculator to graphics calls
# It imports attribute lists and graphics objects
# used by graphics
import sys
import subprocess
import graphics as g
import random
import re
local_vars = {}

class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

"""translates user input into (logical notation)
    - parse works recursively, applying functions and operators
    - variables in logical form are stored in local_vars
        - these variables are tied to an attribute list
        - a variable can represent an existing shape or a hypothetical shape"""
def runMainParser(cmd):
    global local_vars
    local_vars={}
    cmd = clean(cmd)
    # bitpar
    cmd = subprocess.check_output("sh ../bitpar/parse '"+cmd+"'",shell=True)
    cmd = re.sub('\n','',cmd)
    cmd = label(cmd)
    print 'cmd: '+cmd
    print "update input.txt"
    # update input.txt
    subprocess.call("cp ../lambda/lambda-defs.txt ../lambda/input.txt",shell=True)
    subprocess.call("echo '"+cmd+"' >> ../lambda/input.txt",shell=True)
    print "lambda calc"
    # lambda calculator & plop
    subprocess.call("java -jar ../lambda/HCI-auto.jar ../lambda/input.txt > ../lambda/input.tex",shell=True)
    subprocess.call("make -C ../lambda input.fml",shell=True)
    fml = subprocess.check_output('cat ../lambda/input.fml',shell=True)[:-1]
    print "fml: "+fml
    if fml == '': raise ParseError(cmd+' cannot be interpreted by lambda calculator')
    lambdaCalc_output=fml.split('true ')[1][:-2]
    #lambda_output_history.append(lambdaCalc_output) #out of scope. how do i fix this?
    print lambdaCalc_output
    parse(lambdaCalc_output)

def clean(cmd):
    cmd = re.sub('next to', 'next-to', cmd)
    cmd = re.sub('on top of', 'on-top-of', cmd)
    cmd = re.sub('to the left of','to-the-left-of',cmd)
    cmd = re.sub('to the left','to-the-left',cmd)
    cmd = re.sub('to the left side of','to-the-left-side-of',cmd)
    cmd = re.sub('to the right of','to-the-right-of',cmd)
    cmd = re.sub('to the right','to-the-right',cmd)
    cmd = re.sub('to the right side of','to-the-right-side-of',cmd)
    cmd = re.sub('on top of','on-top-of',cmd)
    cmd = re.sub('next to','next-to',cmd)
    cmd = re.sub('inside of','inside-of',cmd)
    cmd = re.sub('in the middle of','in-the-middle-of',cmd)

    return cmd

def label(cmd):
    # see lambda-defs.txt for explanation of labels
    cmd = cmd.replace('make][.DP', 'make1][.NP')
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
    elif string == 'it':
        # print 'it: ',references[0]
        return g.it

    # operators
    elif string.find('\gamma') == 0:
        return gamma(string[7],string[9:-1])
    elif string.find('\iota') == 0:
        # treating iota as gamma for now
        return iota(string[6],string[8:-1])

    # function application
    else:
        fun = string.split( '(' , 1)[0]
        arg = parse(string.split( '(' , 1)[1][:-1])
        exec(fun+'(arg)')

def draw(var):
    """creates a new shape with attList associated with var"""
    attList=local_vars[var]
    g.createShape(attList)

def hide(id):
    """hides the existing shape associated with id"""
    if type(id) is int: # shapeID
        g.hide(g.database[id])
    else: # id refers to hypothetical shape
        shapeID=pickShape(local_vars[id])
        g.hide(g.database[shapeID])
    
def itParamaters(id):
    """fills unspecified attributes of var with attributes of references[0]"""
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'attributes ')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'attributes ')
    for attribute in it:
            g.updateAttList(shape, it[attribute])

def one2(id):
    """returns: most recently mentioned shape with properties in shape"""
    pass


#OPERATORS:
def gamma(var, string):
    """returns: var tied to a new shape with attributes described in string"""
    global local_vars
    #create a new local variable
    local_vars[var]=g.AttributeList()
    #apply functions to new local variable, updating its attibute list
    for substring in string.split(" & "):
        parse(substring)
    return var

def iota(var, string):
    """returns: shapeID of the unique shape matching attributes in string
       throw error: "iota ambiguity" if there is not a unique shape"""
    global local_vars
    local_vars[var]=g.AttributeList()
    for substring in string.split(" & "):
        parse(substring)
    matches = g.database.findMatches(local_vars[var])
    if len(matches) != 1: raise ParseError('iota ambiguity')
    shapeID = matches[0]
    return shapeID

#COLORS:
def red(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'red')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'red')
def orange(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'orange')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'orange')
def yellow(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'yellow')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'yellow')
def green(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'green')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'green')
def blue(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'blue')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'blue')
def purple(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'purple')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'purple')
def white(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'white')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'white')
def black(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'black')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'black')

#SIZES:
def tall(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'tall')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'tall')
def short(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'short')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'short')
def wide(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'wide')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'wide')
def narrow(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'narrow')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'narrow')
def big(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'large')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'large')
def small(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'small')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'small')

#LOCATIONS:
def left(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'left')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'left')
def right(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'right')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'right')
def up(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'up')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'up')
def down(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'down')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'down')

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
def over(id1,id2):
    shape1=getShape(id1)
    shape2=getShape(id2)
    loc= lambda (x,y): y > shape2['center'] + (shape2['span'][1]/2 + shape1['span'][1]/2)
def insideOf(id1,id2):
    pass

#KINDS:
def circle(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'circle')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'circle')
def square(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'square')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'square')
def triangle(id):
    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, 'triangle')
        g.updateShape(id,attList)
    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, 'triangle')
    

#HELPERS:
# def getShape(id):
#     if type(id) is int: # shapeID
#         return shapes[id].get()
#     elif type(id) is str: and len(id) == 1: # local var
#         return local_vars[id]
#     else: # name
#         return shapes[g.names[id]].get()

def pickShape(attList):
    """returns: random shapeID for a shape matching attList"""
    options = g.findMatches(attList)
    return random.choice(options)
    

if __name__ == "__main__":
    # parse("draw(\gamma y(large(y) & square(y))).")
    # runMainParser("put the square next to the circle")
    runMainParser(sys.argv[1])
