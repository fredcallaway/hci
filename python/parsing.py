#!/usr/bin/python

#This module contains the parsing functions
# from Lambda Calculator to graphics calls
# It imports attribute lists and graphics objects
# used by graphics

import graphics
from bash import bash
import re
local_vars = {}
class ParseError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def runMainParser(cmd):
    global local_vars
    local_vars={}
    """translates user input into (logical notation)
        - parse works recursively, applying functions and operators
        - variables in logical form are stored in local_vars
            - these variables are tied to an attribute list
            - a variable can represent an existing shape or a hypothetical shape
    """
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
        return string 
    # if string in names:
        # return string

    # operators
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

def draw(attr):
    print 'draw:'
    print local_vars[attr]
def make1(attr):
   print 'Gui.create()'

def make2(shape, string):
    """updates shape with non-null attributes in attr"""
    pass

def gamma(var,string):
    """returns variable associated with attribute list from attributes in string"""
    global local_vars
    #create a new local variable
    local_vars[var]=graphics.Attributes()
    #apply functions to new local variable, updating its attibute list
    for substring in string.split(" & "):
        parse(substring)
    return var

def iota(var, string):
    """goes through existing shapes and finds ones that matches attributes in string
    if there is one shape that matches, assign var to that shape
    else, throw error: "iota ambiguity"""
    pass

#COLORS:
def red(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'red')
def orange(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'orange')
def yellow(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'yellow')
def green(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'green')
def blue(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'blue')
def purple(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'purple')
def white(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'white')
def black(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'black')

#SIZES:
def tall(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'tall')
def short(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'short')
def wide(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'wide')
def narrow(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'narrow')
def large(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'large')
def small(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'small')

#SHAPES:
def circle(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'circle')
def square(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'square')
def triangle(var):
    global local_vars
    graphics.setAttributes(local_vars[var],'triangle')



if __name__ == "__main__":
    # parse("draw(\gamma y(large(y) & square(y))).")
    runMainParser("make a red triangle")
    # runMainParser("put the square next to the circle")