# Symbolic HCTL model checker

This is the implementation of the first fully symbolic Model Checker for the logic HCTL.
As an input, it takes Boolean network with (possibly unknown) inputs and HCTL formula representing the property we want to check.
It computes all the coloured-states that satisfy the formula.

It is a command line application, the usage is following:
python3 model_check.py model_file hctl_formula

# Inputs and models

The tool takes models in the bnet format as input, with many examples present in bnet_examples/ directory. 

The grammar for HCTL is specified in file src/Parsing_HCTL_formula/HCTL.g4

# Code structure

The main script to run is the model_check.py.

Implementation of the formula components evaluation (EX, binder...) is located in the implementation.py. 
The file also includes all kinds of result printing.

In the Parsing_HCTL_formula/ directory, there is the grammar and parser for the HCTL. 
In the evaluator_hctl.py, there is the main algorithm for the model checker, which includes caching and optimizations.
Most of the other files in the folder is generated automatically from the grammar by ANTLR.

In the Parsing_update_fns/, there is similar grammar, parser and evaluator for the update functions of Boolean network' variables.

The file parse_all.py handles the whole parsing process, of both the Boolean network model and HCTL formula.
This includes the canonization procedure.

In the abstract_syntax_tree.py and model.py, the main data structures can be found.

# Setup

Libraries used: https://github.com/tulip-control/dd, https://github.com/antlr/antlr4/blob/master/doc/python-target.md

DD + CUDD  
$ pip install cython

$ pip download dd --no-deps  
$ tar xzf dd-\*.tar.gz  
$ cd dd-\*/  
$ python setup.py install --fetch --cudd  


ANTLR for generating parser scripts from grammar (NOT needed for simple usage)
$ cd /usr/local/lib  
$ wget https://www.antlr.org/download/antlr-4.9.2-complete.jar  
$ export CLASSPATH=".:/usr/local/lib/antlr-4.9.2-complete.jar:$CLASSPATH"  
$ alias antlr4='java -jar /usr/local/lib/antlr-4.9.2-complete.jar'  
$ alias grun='java org.antlr.v4.gui.TestRig'  

ANTLR for runtime
$ pip install antlr4-python3-runtime

sudo might be needed for the wget or pip

might be needed to include stuff into the pythonpath (or path), using something like: $ export PYTHONPATH="${PYTHONPATH}:~/HCTL_stuff/venv/lib/python3.8/site-packages"

generating scripts from the grammar: $ antlr4 -Dlanguage=Python3 -visitor update_fn.g4  


TERMCOLOR  
$ pip install termcolor  


TIMEOUT DECORATOR  
$ pip install timeout-decorator
