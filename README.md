# CloneResourceMachine v1.0.0
A program that is clone of a game about programming. While the real game has fancy visuals, this is just the backend input-output processing machine.

Presumably the game is a way to teach people programming. And while I claim to already know how to program, it is interesting enough to use a "language" that forces me to think differently, especially when trying to optimize for the challenge parameters (see below). 

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




