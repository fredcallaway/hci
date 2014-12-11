<!--  outline: https://workflowy.com/s/d60IwHWlqj   >   Writeup -->
#Introduction
Stacy is going to write a bomb-ass intro

#PipeLine
<!-- flow diagram here -->
##Overview

## Syntax

## Semantics
For this project, we wanted to translate English sentences to Python commands, and thought that the best way to do that would be through the logical notation of the Lambda Calculus provided by the Lambda Calculator. We considered simply bypassing the logical notation step of the project in favor of simply inputting English into Python, but we ultimately decided to use it. Although inputting parsed text directly into python is much simpler, we prioritized creating a real, semantically viable world. To make this so, we wanted Python to interpret logical notation instead of just taking a certain number of pre-programmed English sentences.

The extra step of pushing the English through the Lambda Calculator makes expansion of this project to a larger lexicon or other languages much easier. Using lambda calculus also allowed us to make many crucial semantic judgments about the words that let the world *shape* up as we wanted.

One of the theoretical semantic choices that we made in this project was the creation and use of the Gamma Operator on indefinite articles. The idea for the Gamma operator came from having a problem with the semantic analysis of the predicates of imperatives. When evaluating sentences beginning with *draw* or *make*, we wanted the type to be consistent across *make the...* sentences and *draw a...* sentences.

Given that we already had an Iota operator for definite articles of type `<et,e>`, it made sense to write our imperative predicates as type `<et>`, and the objects of the imperatives as type `e`. This interpretation required creating a way to make object phrases beginning with the indefinite article type `e`.

When we looked through the definitions of indefinite articles that we had previously used, we saw that they were represented either as an identity function or with the existential quantifier. Neither of these configurations returned the correct type to apply correctly to our `<et>` definition of imperative predicates. We wanted something that would act similarly to the existential quantifier in checking that an element with the correct attributes exists, but we wanted it to return that element, not just a truth value.

Our solution was to represent the indefinite article as a choice function by the Gamma operator. When implemented, the function looks through the whole set of things that match the properties it is fed, and chooses one to return. We added this functionality to the Lambda Calculator program by creating a new operator that was set to evaluate similarly to the Iota operator, but return a Gamma instead.

Another stylistic semantic choice that we made in this project was to represent all properties of objects as function. We set up the lexicon such that all the attributes of an object - including its shape, color,
size, etc. are predicates. This means that when any shape entity is created, it has default properties which can be overridden by calling the functions represented by any of the attribute options. This allows updating properties much easier than if it was simply an attribute of the object itself. Because of this, we are able to evaluate commands such as *"Make the red circle blue"* as `blue(Iota x(red(x))`, and similarly *"Move the red circle left"* as `left(Iota x(red(x))`.

In the semantic definitions file, there are often multiple English words defined with the same logical notation and command. An example of this is that all the words for making things disappear (*delete, remove, erase*) are defined by using the function `hide(x)`, and all the words to make an object larger (*big, bigger, enlarge*) are defined as `big(x)`. This allowed us to create one function that can be applied to different objects and act the same. We tried to anticipate many different words or phrases that a user would naturally use to describe the actions of a drawing program and categorize them into as few functions as possible.

A goal of ours in this project was to allow the user to use language to talk about the shapes as naturally as possible and still have the program understand what objects are being referenced. To accomplish this, we added some features that simulate conversational pragmatic objects.

We identified that there are multiple pragmatic uses of the word *one*.
Based our categorization of which kind of *one* the user wanted, we called different functions. To determine what we thought the user wanted, we called on the the C-commanding verb---either *draw*, *make1*,
or *make2*---and redefined the words accordingly.

When *one* is c-commanded by *draw* or *make1*, the command is interpreted as create a new shape and fill the attributes with the same attributes as the object stored in `it`, a variable pointing to the most recently mentioned object. We imagine this one will be used as a follow up draw command where the user first says *"Make a red triangle. Make a blue one."*

However, when *one* follows *make2*, it looks for the most recently edited existing shape that matches the attributes specified in the command. This would be a sentence such as "Make the red one blue."

Additionally, we wanted our program to be able to use words such as *it*, *that*, and *them* which refer to an object or objects recently referenced in conversation. To do so, we created variables (*it* and *them*) in Python which hold the referents so that the program can access them later. This simulates pragmatic prominence and allows the program to act as if it knows the context of sentences rather than just parsing them as individual worlds. *Them* is essentially an expanded version of *it* and can be used to reference a larger group of entities.

Originally, we thought *it* and *one* would both reference the object in `it`, but we realized that they have different uses. *It* is the object itself, while *one* just accesses the Python attributes of a certain entity, be it either `it`, or a pragmatically relevant entity. The command: *Make a red one* tells the program to make an object with the same attributes as the entity store in `it` and update the color to red. On the other hand, the command *Delete it* tells the program to hide the on screen entity referenced in `it`.

To define *that*, we created it as type `t` for use only with *undo* or *copy*. It refers to the entire last command given to the program. We could expand this in the future to have more referents, but this seemed like the most useful for the scope of this project.

There were many different ambiguities that we differentiated between over the course of defining our lexicon, but we did not handle everything. We did not use some directional statements such as *on top of* because it can mean both *over* and *inside of*. We did not have a clear way to distinguish between the two readings in our universe, and we did not have group consensus on the true meaning of the phrases.

We encountered some semantic challenges while trying to define this new semantic world. We could not get sentences such as *"draw a square and a triangle"* to run properly through the Lambda Calculator. We had *and-e*
defined as a conjunction of type `<e,<ee>>`, and the definition exactly matched the other conjunction words, but the Calculator could not identify the type of the object entity. We hypothesized that this happened because the combination of the two entities creates a new entity (the mereological sum of the entities) that is not in the model,
and it cannot recognize the new entity.

Another type clash we ran into was in commands such as: *"make the triangle a square"*. This is a sentence that should run, but because of the way we defined the words and assigned types to them, it creates a problem. When you run the derivation of the sentence, both *the triangle* and *a square* are type `e`. In order to fix this problem, we'd either have to completely redefine our concept of shapes (have square1 be type `e` and square2 be type `<e,t>`) or define `make3/convert` as a function that takes in two entities and updates the shape property of the first object such that it is equal to the shape property of the second object.

## Action
once lc and `fml` have generated a logical form for the input command, it must be translated into a direction for the gui (i.e. `graphics.py` functions). this is the job of `parsing.parse()`. the main design decision for `parse` was to make it map as transparently as possible onto the predicate logic: every predicate and operator has a corresponding python function. thus, prs works recursively to handle the embdedded functions of predicate logic. at each step, parse is called on a string which is roughly a "constituent" of predicate logic. the leading predicate or operator is then interpreted as a function, with the rest of the string as an argument. the base case of prs is a variable---in the current implementation, these are always local variables binded by operators, but they could theoretically be names that map directly to an existing shape.

### Types and data structures
There are four main classes that represent shapes:

`Shape`
:   
`HypotheticalShape`
`AttributeList`
`Set`

there are two main types of functions used by `parse`: predicates and operators. both the form and purpose of predicates and operators differ, so they require different handling by python.

###predicates
because predicates come in the form `predicate(argument)`, `prs` can treat these directly as functions using the `exec()` command. if the string to be parsed leads with a predicate, `prs` calls the named function on the rest of the string. the argument may be complex, however, thus it must be parsed before it can be passed to the predicate. this defines the basic recursive structure.

one of the key theoertical decision we made was to use predicates as commands and desciptors. for example, in the command `green(\iota x(red(x) & square(x)))`,  red is acting as a desciptor by specifying the shape picked out by `iota` and green is acting as a command by telling the gui to change the color of "the red square" to green. although their basic purpose differs, they are the same kind of predicate in the predicate logic, and thus they are the same kind of function in python.

the observant reader may wonder why we have used "kind" here rather than type. the answer is that `green` and `red` are not actually of the same type in a strict sense. because python is dynamically typed, there is only one definition for each predicate, but observing `parsing.applyPredicate()`, we see that a predicate can, in fact, take four different input types. does this mean that we are following the transparency principle in name only? not quite. with the exception of `Set`, which will be discussed later, these types are all describing essentially the same thing, a shape. the different types exist purely for the sake of following standard coding conventions (e.g. not directly modifying the objects of another module). theoretically, however, they are equivalent, and the code could be written so as to collapse these three.

the final type, `Set` is the only serious contender for the violation of tranpsarency, but even here, we can interpret this as equivalent to the other types if we accept certain theoretical assumptions. specifically, if we interpret all entities as sets, then all predicates take sets as well. under this view, a `HypotheticalShape` or a `shapeID` is really just shorthand for a singleton set.

###operators
operators are how 






##graphics.py
this
 
# Appendix
##Usage
##Lexicon
| Noun      | Verb             | Det | Adj/Adv  | Prep/PP                         | Conj   | Plural |
|-----------|------------------|-----|----------|-------------------------------|------|--------|
| screen    | draw             | a   | another  | on-the-left-side-of-the-screen  | and-et | -s      |
| circle    | make1            | an  | red      | on-the-right-side-of-the-screen | and-t  |        |
| square    | make2            | the | orange   | at-the-top-of-the-screen        |        |        |
| triangle  | delete           |     | yellow   | at-the-bottom-of-the-screen     |        |        |
| oval      | remove           |     | green    | to-the-right                    |        |        |
| rectangle | erase            |     | blue     | to-the-left                     |        |        |
| it        | undo             |     | purple   | to-the-left-of                  |        |        |
| them      | clear-the-screen |     | white    | to-the-left-side-of             |        |        |
| that      | again            |     | black    | on-the-left-side-of             |        |        |
| one1      | copy             |     | big      | to-the-right-of                 |        |        |
| one2      | move             |     | bigger   | to-the-right-side-of            |        |        |
|           | put              |     | right    | on-the-right-side-of            |        |        |
|           | do               |     | left     | over                            |        |        |
|           | enlarge          |     | small    | on-top-of                       |        |        |
|           |                  |     | smaller  | above                           |        |        |
|           |                  |     | wide     | under                           |        |        |
|           |                  |     | wider    | beneath                         |        |        |
|           |                  |     | narrow   | below                           |        |        |
|           |                  |     | narrower |                                 |        |        |
|           |                  |     | up       |                                 |        |        |
|           |                  |     | down     |    
##Example Sentences
##Implementation Details

 
##Python
The GUI is a Tkinter Entry object cmd line interface coupled with a Tkinter Canvas object for display and Text object for history. The cmd line accepts natural language input, and the Canvas serves as the graphical interface. 

### Module structure
#### main 
      - Handles Tk window and frame, initializes graphics and callbacks 
      - cmdLineCallback() controls the behavior of the cmd line interface; it calls runMainParser() from the parsing module to initiate Canvas state change 
      - Contains handling for cmd line history (Up Down keys) and a Python code parser 
  - parsing 
      - runMainParser(cmd)) 
         - uses the Subprocess module to open a Shell and run bitpar/bitpar, lambda/HCI- auto.jar, and other shell commands to generate a lambda parsing of the user input 
      - The module contains various functions to handle operators defined in lambda- defs.txt, based on those names 
      - The functions operate on ShapeID or AttributeList objects, imported from graphics module. These classes are used to describe variables in lambda calculus, referencing newly created graphical objects (AttributeList) or existing ones (ShapeID). 
  - graphics 
      - AttributeList class 
         - This class describes every existing or hypothetical graphical object. It is a dictionary for string keys (matching lamdba definitions for enumerated properties), and also has local geometrical fields for its center and span vectors. The Canvas is assumed to be a plane with (0,0) at its center. 
      - relational, change, and attribute Types 
         - these specify mappings from a lambda keyword to change on an AttributeList object. For relational and change Types, a function mapped to the change name is applied to the arguments of the predicate. For attribute types, the AttributeList dictionary is updated by the attribute change, if the change name does not match a relation or change type. The type names are described in a 2D tuple array. 
      - updateAttList(attList,command) 
         - compares command to relational, change, and attribute types and changes the AttributeList attList according to the functons or dictionary values mapped to by the 2D tuple array. 
      - Shape class 
         - This class represents objects drawn on the Canvas. When a createShape(attList) method is called, an attribute list is drawn to the Canvas as an image, and the Tkinter Canvas ID of the image is store with the attribute list. This list is the used to initialize a Shape object, which is added to the database. The createShape method returns a shapeID associated with the Shape object 
         - A Shape can be updated with a new attribute list 
      - database = HistoryMap() 
         - The database is a dictionary from shapeIDs to Shape objects. It is a HistoryMap for legacy naming reasons. In reality, the Shape objects containt their own history, and also undo(), redo(), and update(attList) methods which cycle through shape history. This allows us to update the screen by hiding previous shape images and unhiding new ones. Below is the schematic for referncing the description and Tkinter image ID of a shape reference: 
         - database[shapeID] - > Shape shape 
- contains history of attribute lists 
         - shape.getAttList() - > AttributeList attList 
- describes the current shape 
         - attList.imageID - > Tkinter Canvas id of the current image 
- used for graphical commands 
         - The database is generally modified by functions in graphics to ensure consistency with the Canvas. 
      - create/update Shape method (attribute list/shapeID) 
         - This set of methods in graphics updates the database and the canvas in a consisten manner. It also assigns the graphics.it variable to the shapeID of the latest shape modified 
      - The above schematic allows us to go from attribute lists and shape references to graphical control through Tkinter ID references. The drawAttList(attList) command creates a new image to update Shapes with, the hide/unhide(shapeID) functions remove images from the Canvas, and are used by the undo/redo(shapeID) functions in conjunction with undo and redo for the Shape object itself 




##Examples

