#!/usr/bin/pythont.

#This module contains the parsing functions
# from Lambda Calculator to graphics calls
# It imports attribute lists and graphics objects
# used by graphics

import graphics
#from bash import bash
import re
local_vars = {}
shapes = []
named_shapes = {}
class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)





"""translates user input into (logical notation)
    - parse works recursively, applying functions and operators
    - variables in logical form are stored in local_vars
        - these variables are tied to an attribute list
        - a variable can represent an existing shape or a hypothetical shape
"""
def runMainParser(cmd):
    global local_vars
    local_vars={}
    
    # bitpar
    cmd=clean(cmd)
    cmd=str(bash("sh ../bitpar/parse '"+cmd+"'"))
    cmd=label(cmd)
    print cmd

    # update input.txt
    bash("cp ../lambda/lambda-defs.txt ../lambda/input.txt")
    bash("echo '"+cmd+"' >> ../lambda/input.txt")

    # lambda calculator & plop
    bash("java -jar ../lambda/lambda-auto.jar ../lambda/input.txt > ../lambda/input.tex")
    bash("make -C ../lambda input.fml")
    fml=`bash('cat ../lambda/input.fml')`
    if fml == '': raise ParseError('cannot be interpreted by lambda calculator')

    lambdaCalc_output=fml.split('true ')[1]
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
    print "parse("+string+")"
    # variables
    if string in local_vars: # e.g. 'y'
        return local_vars[string]
        print local_vars[string]
    # elif string in named_shapes:
        # return named_shapes[string]
    # elif string is 'it':
        # return graphics.it

    # operators
    # this is essentially binding
    elif string.find('\gamma') == 0:
        return gamma(string[7],string[9:len(string)-2])
    elif string.find('\iota') == 0:
        # treating iota as gamma for now
        return gamma(string[6],string[8:len(string)-2])

    # function application
    else:
        fun = string.split( '(' , 1)[0] # e.g. 'draw' or 'red'
        arg = parse(string.split( '(' , 1)[1][:-1])  # e.g. 'Gy[(red(y) & square(y)]' or 'y'
        exec(fun+'(arg)')

def draw(shape):
    #creates a new shape
    print 'drawing: '+shape
    # graphics.drawAttributes(shape)

def one1(shape):
    #fills unspecified attributes of var with attributes of graphics.it
    for attribute in it():
            graphics.updateAttributes(shape, graphics.it[attribute])

def one2(shape):
    #returns: most recently mentioned shape with properties in shape
    pass

def gamma(var,string):
    #returns: a new shape with attributes described in string
    global local_vars
    #create a new local variable
    #local variables are keys for local_vars
    local_vars[var]=graphics.Attributes()
    #apply functions to new local variable, updating its attibute list
    for substring in string.split(" & "):
        parse(substring)
    return local_vars[var]

def iota(var, string):
    #returns: the unique shape matching attributes in string
    #   throw error: "iota ambiguity" if there is not a unique shape
    global local_vars
    local_vars[var]=graphics.Attributes()
    for substring in string.split(" & "):
        parse(substring)
    matches = graphics.findMatches(local_vars[var])
    if len(matches) != 1: raise ParseError('iota ambiguity')
    idnum = matches[0][0]
    return shapes[idnum]

#COLORS:
def red(shape):
    graphics.updateAttributes(shape, 'red')
def orange(shape):
    graphics.updateAttributes(shape, 'orange')
def yellow(shape):
    graphics.updateAttributes(shape, 'yellow')
def green(shape):
    graphics.updateAttributes(shape, 'green')
def blue(shape):
    graphics.updateAttributes(shape, 'blue')
def purple(shape):
    graphics.updateAttributes(shape, 'purple')
def white(shape):
    graphics.updateAttributes(shape, 'white')
def black(shape):
    graphics.updateAttributes(shape, 'black')

#SIZES:
def tall(shape):
    graphics.updateAttributes(shape, 'tall')
def short(shape):
    graphics.updateAttributes(shape, 'short')
def wide(shape):
    graphics.updateAttributes(shape, 'wide')
def narrow(shape):
    graphics.updateAttributes(shape, 'narrow')
def large(shape):
    graphics.updateAttributes(shape, 'large')
def small(shape):
    graphics.updateAttributes(shape, 'small')

#SHAPES:
def circle(shape):
    graphics.updateAttributes(shape, 'circle')
def square(shape):
    graphics.updateAttributes(shape, 'square')
def triangle(shape):
    graphics.updateAttributes(shape, 'triangle')
    


if __name__ == "__main__":
    # parse("draw(\gamma y(large(y) & square(y))).")
    # runMainParser("make a red triangle")
    # runMainParser("put the square next to the circle")
    runMainParser("make the red triangle")

