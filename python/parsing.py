<<<<<<< HEAD
#!/usr/bin/python
"""This module contains the parsing functions from predicate logic to graphics.py calls"""

import sys
import subprocess
import graphics as g
import random
import re
local_vars = {} #map from vars to attLists and Sets

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

class Set():
    """represents a set of shapeIDs as defined by an attList"""
    
    def __init__(self,var):
        assert type(var) is str
        self.attList = local_vars[var]
        local_vars[var] = self
    def getShapeIDs(self):
        matches = g.database.findMatches(self.attList)
        return matches

def runMainParser(cmd):
    """updates one or more shapes in the gui based on user input

    uses the Subprocess module to open a Shell and run bitpar/bitpar, 
    lambda/HCI-auto.jar, and other shell commands to generate a 
    lambda parsing of the user input"""

    global local_vars
    local_vars={}
    # pre-process phrase to group keyword sequences
    cmd = hyphenate(cmd)
    cmd = pluralize(cmd)
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
    if fml == '' or fml == '  {result \\ $tt$ \\': raise ParseError(cmd+' cannot be interpreted by lambda calculator')
    lambdaCalc_output=fml.split('true ')[1][:-2]
    #lambda_output_history.append(lambdaCalc_output) #out of scope. how do i fix this?
        #lambda_output_history was never initialized
    print 'logic: '+lambdaCalc_output
    parse(lambdaCalc_output)

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
    cmd = re.sub('at the top','at-the-top',cmd)
    cmd = re.sub('to the top','to-the-top',cmd)
    cmd = re.sub('at the bottom','at-the-bottom',cmd)
    cmd = re.sub('to the bottom','to-the-bottom',cmd)
    cmd = re.sub('in the middle','in-the-middle',cmd)
    cmd = re.sub('to the middle','to-the-middle',cmd)

    cmd = re.sub('and t','and-t',cmd)
    cmd = re.sub('and et','and-et',cmd)
    cmd = re.sub('clear the screen','clear-the-screen',cmd)
    return cmd

def pluralize(cmd):
    """returns: cmd with plural 's' separated by a space"""
    # in the future this could be automated
    cmd = re.sub('circles','circle s',cmd)
    cmd = re.sub('squares','square s',cmd)
    cmd = re.sub('triangles','triangle s',cmd)
    cmd = re.sub('ovals','oval s',cmd)
    cmd = re.sub('rectangles','rectangle s',cmd)
    cmd = re.sub('one2s','one2 s',cmd)
    return cmd

def label(cmd):
    """applies labels to differentiate synonyms"""
    cmd = cmd.replace('make][.DP', 'make1][.NP')
    cmd = cmd.replace('make][.SC', 'make2][.SC')
    cmd = re.sub('(draw.*)one','\\1one1',cmd)
    cmd = re.sub('(make1.*)one','\\1one1',cmd)
    cmd = re.sub('(make2.*)one','\\1one2',cmd)
    cmd = re.sub('(move.*)one','\\1one2',cmd)
    cmd = re.sub('(hide.*)one','\\1one2',cmd)
    cmd = '[result ' + cmd + ']' #dummy function for plop
    return cmd


def parse(string):
    """parses a string of logical notation, calling functions as necessary

    - parse works recursively, applying functions and operators
    - variables in logical form are stored in local_vars
        - these variables are tied to an attributeList"""
    
    global local_vars
    print "parse("+string+")"

    # variables
    if string in local_vars: # e.g. 'y'
        return string
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
                or if var is defined to be a Set, return the Set

       throws error: "iota ambiguity" if there is not a unique shape"""
    global local_vars
    local_vars[var]=g.AttributeList()
    for substring in string.split(" & "):
        parse(substring)
    if isinstance(local_vars[var], Set):
        return local_vars[var]
    else: 
        matches = g.database.findMatches(local_vars[var])
        if len(matches) != 1: raise ParseError('iota ambiguity')
        shapeID = matches[0]
        return shapeID

#PRAGMATIC
def one1(var):
    """fills unspecified attributes of var with attributes of most recently mentioned shape"""
    varAttList = local_vars[var]
    itAttList = g.getIt()
    local_vars[var] = g.AttributeList(itAttList.items() + varAttList.items())

def one2(var):
    """fills unspecified attributes of var with attributes of 
    most recently mentioned shape that matches attributes in var"""
    varAttList = local_vars[var]
    options = g.database.findMatches(local_vars[var])
    shapeAttList = g.database[g.referenceOrder.pickMostRecent(options)].getAttList()
    local_vars[var] = g.AttributeList(shapeAttList.items()+ varAttList.items())

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
def large(id):
    applyPredicate(id,'big')
def small(id):
    applyPredicate(id,'small')

def taller(id):
    applyPredicate(id,'taller')
def shorter(id):
    applyPredicate(id,'shorter')
def wider(id):
    applyPredicate(id,'wideer')
def narrower(id):
    applyPredicate(id,'narrower')
def larger(id):
    applyPredicate(id,'biger')
def smaller(id):
    applyPredicate(id,'smaller')

#LOCATIONS:
def left(id):
    applyPredicate(id,'left')
def right(id):
    applyPredicate(id,'right')
def up(id):
    applyPredicate(id,'up')
def down(id):
    applyPredicate(id,'down')
def over(id):
    applyPredicate(id,'over')

def screenTop(id):
    applyPredicate(id,'screenTop')
def screenBottom(id):
    applyPredicate(id,'screenBottom')
def screenLeft(id):
    applyPredicate(id,'screenLeft')
def screenRight(id):
    applyPredicate(id,'screenRight')
def screenCenter(id):
    applyPredicate(id,'screenCenter')


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
def oval(id):
    applyPredicate(id,'triangle')
def rectangle(id):
    applyPredicate(id,'triangle')
    

#HELPERS:

def pickShape(attList):
    """returns: random shapeID for a shape matching attList"""
    options = g.database.findMatches(attList)
    return random.choice(options)
    
def applyPredicate(id,cmd):
    """applies a predicate to object represented by id

    performs an action depending on type of id:
        - shapeID: updates associated shape with cmd
        - HypotheticalShape: picks a random matching shape
          and updates it with cmd
        - Set: updates all shapeIDs with cmd
        - var: updates attList associated with var"""

    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, cmd)
        g.updateShape(id,attList)

    elif type(id) is HypotheticalShape:
        attList = id.getAttList()
        try:
            shapeID=pickShape(attList)
            g.updateShape(shapeID,attList)
        except IndexError:
            return

    elif type(id) is g.AttributeList:
        attList=id
        try:
            shapeID=pickShape(attList)
            g.updateShape(shapeID,attList)
        except IndexError:
            return

    elif type(id) is str:
         # local var
        attList = local_vars[id]
        g.updateAttList(attList, cmd)

    elif isinstance(id, Set):
        for shapeID in id.getShapeIDs():
            applyPredicate(shapeID, cmd)
    else:
        print "Cannot apply predicate to unknown object 'id'"

if __name__ == "__main__":
    # parse("draw(\gamma y(large(y) & square(y))).")
    # runMainParser("put the square next to the circle")
    runMainParser(sys.argv[1])
=======
#!/usr/bin/python
"""This module contains the parsing functions from predicate logic to graphics.py calls"""

import sys
import subprocess
import graphics as g
import random
import re
local_vars = {} #map from vars to attLists and Sets

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

class Set():
    """represents a set of shapeIDs as defined by an attList"""
    
    def __init__(self,var):
        assert type(var) is str
        self.attList = local_vars[var]
        local_vars[var] = self
    def getShapeIDs(self):
        matches = g.database.findMatches(self.attList)
        return matches

def runMainParser(cmd):
    """updates one or more shapes in the gui based on user input

    uses the Subprocess module to open a Shell and run bitpar/bitpar, 
    lambda/HCI-auto.jar, and other shell commands to generate a 
    lambda parsing of the user input"""

    global local_vars
    local_vars={}
    # pre-process phrase to group keyword sequences
    cmd = hyphenate(cmd)
    cmd = pluralize(cmd)
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
    if fml == '' or fml == '  {result \\ $tt$ \\': raise ParseError(cmd+' cannot be interpreted by lambda calculator')
    lambdaCalc_output=fml.split('true ')[1][:-2]
    #lambda_output_history.append(lambdaCalc_output) #out of scope. how do i fix this?
        #lambda_output_history was never initialized
    print 'logic: '+lambdaCalc_output
    parse(lambdaCalc_output)

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
    cmd = re.sub('at the top','at-the-top',cmd)
    cmd = re.sub('to the top','to-the-top',cmd)
    cmd = re.sub('at the bottom','at-the-bottom',cmd)
    cmd = re.sub('to the bottom','to-the-bottom',cmd)
    cmd = re.sub('in the middle','in-the-middle',cmd)
    cmd = re.sub('to the middle','to-the-middle',cmd)

    cmd = re.sub('and t','and-t',cmd)
    cmd = re.sub('and et','and-et',cmd)
    cmd = re.sub('clear the screen','clear-the-screen',cmd)
    return cmd

def pluralize(cmd):
    """returns: cmd with plural 's' separated by a space"""
    # in the future this could be automated
    cmd = re.sub('circles','circle s',cmd)
    cmd = re.sub('squares','square s',cmd)
    cmd = re.sub('triangles','triangle s',cmd)
    cmd = re.sub('ovals','oval s',cmd)
    cmd = re.sub('rectangles','rectangle s',cmd)
    cmd = re.sub('one2s','one2 s',cmd)
    return cmd

def label(cmd):
    """applies labels to differentiate synonyms"""
    cmd = cmd.replace('make][.DP', 'make1][.NP')
    cmd = cmd.replace('make][.SC', 'make2][.SC')
    cmd = re.sub('(draw.*)one','\\1one1',cmd)
    cmd = re.sub('(make1.*)one','\\1one1',cmd)
    cmd = re.sub('(make2.*)one','\\1one2',cmd)
    cmd = re.sub('(move.*)one','\\1one2',cmd)
    cmd = re.sub('(hide.*)one','\\1one2',cmd)
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
                or if var is defined to be a Set, return the Set

       throws error: "iota ambiguity" if there is not a unique shape"""
    global local_vars
    local_vars[var]=g.AttributeList()
    for substring in string.split(" & "):
        parse(substring)
    if isinstance(local_vars[var], Set):
        return local_vars[var]
    else: 
        lvar = local_vars[var]
        if type(lvar) is g.AttributeList:
            matches = g.database.findMatches(lvar)
        elif type(lvar) is int:
            matches = g.database.findMatches(g.database[lvar].getAttList())
        else:
            print "Cannot find matches for type %s"%type(lvar)
        if len(matches) != 1: raise ParseError('iota ambiguity')
        shapeID = matches[0]
        return shapeID

#PRAGMATIC
def one1(var):
    """fills unspecified attributes of var with attributes of most recently mentioned shape"""
    varAttList = local_vars[var]
    itAttList = g.getIt()
    local_vars[var] = g.AttributeList(itAttList.items() + varAttList.items())

def one2(var):
    """fills unspecified attributes of var with attributes of 
    most recently mentioned shape that matches attributes in var"""
    varAttList = local_vars[var]
    options = g.database.findMatches(local_vars[var])
    shapeAttList = g.database[g.referenceOrder.pickMostRecent(options)].getAttList()
    local_vars[var] = g.AttributeList(shapeAttList.items()+ varAttList.items())

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
def large(id):
    applyPredicate(id,'big')
def small(id):
    applyPredicate(id,'small')

def taller(id):
    applyPredicate(id,'taller')
def shorter(id):
    applyPredicate(id,'shorter')
def wider(id):
    applyPredicate(id,'wider')
def narrower(id):
    applyPredicate(id,'narrower')
def larger(id):
    applyPredicate(id,'biger')
def smaller(id):
    applyPredicate(id,'smaller')

#LOCATIONS:
def left(id):
    applyPredicate(id,'left')
def right(id):
    applyPredicate(id,'right')
def up(id):
    applyPredicate(id,'up')
def down(id):
    applyPredicate(id,'down')
def over(id):
    applyPredicate(id,'over')

def screenTop(id):
    applyPredicate(id,'screenTop')
def screenBottom(id):
    applyPredicate(id,'screenBottom')
def screenLeft(id):
    applyPredicate(id,'screenLeft')
def screenRight(id):
    applyPredicate(id,'screenRight')
def screenCenter(id):
    applyPredicate(id,'screenCenter')


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
def oval(id):
    applyPredicate(id,'triangle')
def rectangle(id):
    applyPredicate(id,'triangle')
    

#HELPERS:

def pickShape(attList):
    """returns: random shapeID for a shape matching attList"""
    options = g.database.findMatches(attList)
    return random.choice(options)
    
def applyPredicate(id,cmd):
    """applies a predicate to object represented by id

    performs an action depending on type of id:
        - shapeID: updates associated shape with cmd
        - HypotheticalShape: picks a random matching shape
          and updates it with cmd
        - Set: updates all shapeIDs with cmd
        - var: updates attList associated with var"""

    if type(id) is int: # shapeID
        attList = g.database[id].getAttList()
        g.updateAttList(attList, cmd)
        g.updateShape(id,attList)

    elif type(id) is HypotheticalShape:
        attList = id.getAttList()
        try:
            shapeID=pickShape(attList)
            g.updateShape(shapeID,attList)
        except IndexError:
            return

    elif type(id) is g.AttributeList:
        attList=id
        try:
            shapeID=pickShape(attList)
            g.updateShape(shapeID,attList)
        except IndexError:
            return

    elif type(id) is str:
         # local var
        attList = local_vars[id]
        g.updateAttList(attList, cmd)

    elif isinstance(id, Set):
        for shapeID in id.getShapeIDs():
            applyPredicate(shapeID, cmd)
    else:
        print "Cannot apply predicate to unknown object 'id'"

if __name__ == "__main__":
    # parse("draw(\gamma y(large(y) & square(y))).")
    # runMainParser("put the square next to the circle")
    runMainParser(sys.argv[1])
>>>>>>> 092078ad2b8e1d35517d03bb271c6b98b9c675ad
