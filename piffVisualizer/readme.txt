The actual science of logic is conversant at present only with things either
certain, impossible, or entirely doubtful, none of which (fortunately) we
have to reason on. Therefore the true logic for this world is the calculus
of Probabilities, which takes account of the magnitude of the probability
which is, or ought to be, in a reasonable man’s mind.
James Clerk Maxwell (1850)

---- readme starts here ----

I will briefly explain the files listed in this directory:

compactPIF.py: this compiles all of the pif files in the current folder (now 6) to a binary file format in alphabetical order. 
The output (the file named outputpiff) will then contain all of the frames and is now readable by pifVisualiser.

pifVisualizer: You can execute this by running ./pifVisualizer in Linux and it will grab the file outputpiff and display its contents in a sequential manner.

Makefile: These are the compilation instructions for pifVisualizer. To compile simply write: "make" while in this folder.

gridlogic and pifVisualizer are some sloppy cpp files to draw everything, never said it was going to be pretty ;).


---- Please write you desired functionality here ----

- Passive movie rendering
