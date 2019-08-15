# CloneResourceMachine v1.1.0
A program that is clone of a game about programming. While the real game has fancy visuals, this is just the backend input-output processing machine.

Presumably the game is a way to teach people programming. And while I claim to already know how to program, it is interesting enough to use a "language" that forces me to think differently, especially when trying to optimize for the challenge parameters (see below). 

Version 1.1.0 is also the start of a Web API, intended to work with a front end. Django is the intended current target. With also either React or Vue. Although, given enough time, perhaps multiple front end frameworks and multiple back end frameworks as different musings.  

## Basics
The game has a few basic parts:

1. A set of input (the "inbox"), which is some mix of single letters and numbers. 
2. An "outbox" to collect the output from the program.
3. A set of "registers" as temporary storage space. 
4. An active item being worked on ("held in hand").
5. A set of commands that make up the program and what to do with each item.

The command set feels similar to assembly: using instructions that act on the current item in hand, or using "jump to" type instructions, etc.

There is a given task for each level, such as "for each input, put it in the inbox if it is a zero". And there are two challenges, one for speed ("running time" based on how many total commands are executed) and one for size (number of lines in the program). 

It's not always possible use a single program to solve both challenges. Also, while the size challenge is pretty straight forward, the game mentinons that the speed value is based on averaging out the run time for various input. This makes matching their exact speed value in my clone app a challenge (an unmet goal as of version 1). 

## Set Up
Make sure you run the provided `setup_jagpy.py` script (long, boring story) before attempting other code. There is a `requirements.txt` for which to pay attention. And this was last tested with Python 3.6.1.

## Running it

There is a test `tests/confirm_all_levels.py` that will confirm that all levels run in the expected time frame and lines of code. Unit-like tests are available in the `tests/` folder.

But you can also run a specific level with `run.py <level key> <program key>`, where the `<level key>` is one of 1 to 21 (given that we load `levels/game.yaml` non-optionally ATM). The `<program key>` is either `fast` or `small` (technically, `optimal` as well, but not all have optimal solutions: that is where they are both fast and small).

But additional levels with string-like names and alternate programs are possible in the YAML, if one was so inclined to add them.


## Command Sets
(needs more text)



# Lets support these commands:
    #[] `inbox` : get item from inbox
    #[] `outbox`: put item into outbox
    #[] `copyfrom $r`: copy value from register $r
    #[] `copyto $r`: copy value to register $r
    #[] `jump $p|$l`: jump to program line number or label
    #[] `jump_zero $p|$l`
    #[] `jump_neg $p|$l`
    #[] `add`
    #[] `sub`
    #[] `echo $m`
    #[] `# $m`
    #[] `@l`

# Config
    #[] `registers $n`
    #[] `alphabet $a`
    #[] `goal_instructions $n`
    #[] `goal_runtime $n`
    #[] `instruct_set $a`
    #[] `expected $x`
    #[] `input_details $x`

