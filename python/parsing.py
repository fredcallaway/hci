
#!/usr/bin/python

"""This module contains the parsing functions from predicate logic to graphics.py calls"""
import sys
import subprocess
import graphics as g
import random
import re
local_vars = {}

class ParseError(Exception):
    """an error that arises during parsing"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class HypotheticalShape():
    """represents a hypothetical shape created by gamma"""
    def __init__(self,var):
        assert type(var) is str
        self.var = var
    def getAttList(self):
        return local_vars[self.var]

def runMainParser(cmd):
    """translates user input into logical notation"""
    global local_vars
    local_vars={}
    cmd = hyphenate(cmd)
    # bitpar
    cmd = subprocess.check_output("sh ../bitpar/parse '"+cmd+"'",shell=True)
    cmd = re.sub('\n','',cmd)
    cmd = label(cmd)
    print 'syntax: '+cmd
    # update input.txt
    subprocess.call("cp ../lambda/lambda-defs.txt ../lambda/input.txt",shell=True)
    subprocess.call("echo '"+cmd+"' >> ../lambda/input.txt",shell=True)
    # lambda calculator & plop
    subprocess.call("java -jar ../lambda/HCI-auto.jar ../lambda/input.txt > ../lambda/input.tex",shell=True)
    subprocess.call("make -C ../lambda input.fml",shell=True)
    fml = subprocess.check_output('cat ../lambda/input.fml',shell=True)[:-1]
    if fml == '': raise ParseError(cmd+' cannot be interpreted by lambda calculator')
    lambdaCalc_output=fml.split('true ')[1][:-2]
    #lambda_output_history.append(lambdaCalc_output) #out of scope. how do i fix this?
    print 'logic: '+lambdaCalc_output
    # parse(lambdaCalc_output)

def hyphenate(cmd):
    """returns cmd with phrase substitutions for easier parsing"""
    cmd = re.sub('at the top of the screen','at-the-top-of-the-screen',cmd)
    cmd = re.sub('at the bottom of the screen','at-the-bottom-of-the-screen',cmd)
    cmd = re.sub('on the left side of the screen','on-the-left-side-of-the-screen',cmd)
    cmd = re.sub('on the right side of the screen','on-the-right-side-of-the-screen',cmd)
    cmd = re.sub('on the left side of','on-the-left-side-of',cmd)
    cmd = re.sub('to the left side of','to-the-left-side-of',cmd)
    cmd = re.sub('to the left of','to-the-left-of',cmd)
    cmd = re.sub('to the left','to-the-left',cmd)
    cmd = re.sub('to the right side of','to-the-right-side-of',cmd)
    cmd = re.sub('on the right side of','on-the-right-side-of',cmd)
    cmd = re.sub('to the right of','to-the-right-of',cmd)
    cmd = re.sub('to the right','to-the-right',cmd)
    cmd = re.sub('in the middle of','in-the-middle-of',cmd)
    cmd = re.sub('on top of','on-top-of',cmd)
    cmd = re.sub('inside of','inside-of',cmd)
    cmd = re.sub('next to','next-to',cmd)
    cmd = re.sub('and t','and-t',cmd)
    cmd = re.sub('and et','and-et',cmd)
    cmd = re.sub('clear the screen','clear-the-screen',cmd)

    return cmd

def label(cmd):
    """applies labels to differentiate synonyms

    see lambda-defs.txt for explanation of labels"""
    cmd = cmd.replace('make][.DP', 'make1][.NP')
    cmd = cmd.replace('make][.SC', 'make2][.SC')
    cmd = re.sub('(draw.*)one','\\1one1',cmd)
    cmd = re.sub('(make1.*)one','\\1one1',cmd)
    cmd = re.sub('(make2.*)one','\\1one2',cmd)
    cmd = '[result ' + cmd + ']' #dummy function for plop
    return cmd


def parse(string):
    """parses a string of logical notation, calling functions as necessary

    - parse works recursively, applying functions and operators
    - variables in logical form are stored in local_vars
        - these variables are tied to an attributeList"""
    
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

###########
#  WORDS  #
###########

#COMMANDS
def draw(hyp):
    """creates a new shape with hyp's attributes"""
    print 'g.createShape(',hyp.getAttList(),')'
    print type(hyp.getAttList())
    g.createShape(hyp.getAttList())

def hide(id):
    """hides the existing shape associated with id

       note: id refers to either a shapeID or a var"""
    if type(id) is int: # shapeID
        g.hide(g.database[id])
    else: # id refers to hypothetical shape
        shapeID=pickShape(local_vars[id])
        g.hide(g.database[shapeID])
    
def itParamaters(var):
    """fills unspecified attributes of var with attributes of most recently mentioned shape"""
    varAttList = local_vars[var]
    itAttList = g.getIt()
    local_vars[var] = dict(itAttList.items() + varAttList.items())

def one2(var):
    """returns: most recently mentioned shape with properties in shape"""
    options = g.findMatches(local_vars[var])
    return g.referenceOrder.pickMostRecent(options)

#OPERATORS:
def gamma(var, string):
    """returns: a HypotheticalShape with attributes described in string"""
    global local_vars
    # create a new local variable tied to an attList
    local_vars[var]=g.AttributeList()
    # attach this attList to a hypothetical shape
    hyp = HypotheticalShape(var)
    # apply functions to the attList, defining the hypothetical shape
    for substring in string.split(" & "):
        parse(substring)
    return hyp

def iota(var, string):
    """returns: shapeID of the unique shape matching attributes in string

       throws error: "iota ambiguity" if there is not a unique shape"""
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
    applyPredicate(id,'red')
def orange(id):
    applyPredicate(id,'orange')
def yellow(id):
    applyPredicate(id,'yellow')
def green(id):
    applyPredicate(id,'green')
def blue(id):
    applyPredicate(id,'blue')
def purple(id):
    applyPredicate(id,'purple')
def white(id):
    applyPredicate(id,'white')
def black(id):
    applyPredicate(id,'black')

#SIZES:
def tall(id):
    applyPredicate(id,'tall')
def short(id):
    applyPredicate(id,'short')
def wide(id):
    applyPredicate(id,'wide')
def narrow(id):
    applyPredicate(id,'narrow')
def big(id):
    applyPredicate(id,'big')
def small(id):
    applyPredicate(id,'small')

#LOCATIONS:
def left(id):
    applyPredicate(id,'left')
def right(id):
    applyPredicate(id,'right')
def up(id):
    applyPredicate(id,'up')
def down(id):
    applyPredicate(id,'down')

# def leftOf(id1,id2):
#     shape1=getShape(id1)
#     shape2=getShape(id2)
#     # uncertain values are functions that return True if given a value that matches the requirement
#     # TODO: combine functions for "to the left of the triangle and above the square"
#     loc= lambda (x,y): x < shape2['center'] - (shape2['span'][0]/2 + shape1['span'][0]/2)
# def rightOf(id1,id2):
#     shape1=getShape(id1)
#     shape2=getShape(id2)
#     loc= lambda (x,y): x > shape2['center'] + (shape2['span'][0]/2 + shape1['span'][0]/2)
# def below(id1,id2):
#     shape1=getShape(id1)
#     shape2=getShape(id2)
#     loc= lambda (x,y): x < shape2['center'] - (shape2['span'][1]/2 + shape1['span'][1]/2)
# def over(id1,id2):
#     shape1=getShape(id1)
#     shape2=getShape(id2)
#     loc= lambda (x,y): y > shape2['center'] + (shape2['span'][1]/2 + shape1['span'][1]/2)
# def insideOf(id1,id2):
#     pass

#KINDS:
def circle(id):
    applyPredicate(id,'circle')
def square(id):
    applyPredicate(id,'square')
def triangle(id):
    applyPredicate(id,'triangle')
    

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
    
def applyPredicate(id,cmd):
    """applies a predicate to object represented by id

    performs an action depending on type of id:
        - shapeID: updates associated shape with cmd
        - HypotheticalShape: picks a random matching shape
          and updates it with cmd
        - var: updates attList associated with var"""

    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, cmd)
        g.updateShape(id,attList)

    elif type(id) is HypotheticalShape:
        attList = id.getAttList()
        shapeID=pickShape(attList)
        g.updateShape(shapeID,attList)

    else: # local var
        attList = local_vars[id]
        g.updateAttList(attList, cmd)

if __name__ == "__main__":
    # parse("draw(\gamma y(large(y) & square(y))).")
    # runMainParser("put the square next to the circle")
    runMainParser(sys.argv[1])
