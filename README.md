# Symbolic HCTL model checker

This repository contains the implementation of the symbolic model checker for the logic HCTL.
It can be used for the analysis of (partially specified) Boolean networks. In particular, it allows to check for any behavioural hypotheses expressible in HCTL on large, non-trivial networks. This includes properties like stability, bi-stability, attractors, or oscillatory behaviour.

For given Boolean network with (possibly unknown) inputs and HCTL formula (representing the property we want to check), it computes all the states of the network (and corresponding colours) that satisfy the formula.

The usage is following:
```
python3 model_check.py model_file hctl_formula
```

# Inputs and models

The tool takes BN models in the `bnet` format as its input, with many example models present in the `benchmark_models` directory. Benchmark models are also present in the aeon (and often even sbml) formats, but this is just for the convenience of the user and those can't be used as inputs.

The grammar for HCTL is specified in the readable format in the file `src/Parsing_HCTL_formula/HCTL.g4`. Example formulae can be found in the file `formulae_examples.txt`.

# Code structure

The main script to run is the model_check.py.

The model-checking algorithm, together with the caching and optimizations, is implemented in the evaluator_hctl.py.
The evaluation of individual HCTL operators (EX, binder, ...) can be found in the implementation_components.py. 
Evaluation of the update functions of BN variables is handled by evaluator_update_fn.py

In the parse_hctl_formula directory, there is a grammar and parser for the HCTL logic. 
Most of the other files in the folder is generated automatically from the grammar by ANTLR.
Similarly, in the parse_update_function directory, there is a grammar, parser and other things for the update functions of BN variables.

The file parse_all.py handles the whole parsing process, of both the Boolean network model and the HCTL formula.
That includes the canonization procedure of state variables.

In the abstract_syntax_tree.py and model.py, the main data structures can be found.


# Setup

Following steps should work on Linux systems, including WSL. 

We use two main libraries:
- [dd](https://github.com/tulip-control/dd) for the underlying binary decision diagrams implementation
- [ANTLR4](https://github.com/antlr/antlr4/blob/master/doc/python-target.md) for the parser of both HCTL formulae and update functions

To set up ANTLR and some other minor modules and requirements:
```
pip install wheel
pip install -r requirements.txt
```

To achieve the best perfomance, we have to use the CUDD bindings of the dd library:
```
pip download dd --no-deps  
tar xzf dd-\*.tar.gz  
cd dd-\*/  
python setup.py install --fetch --cudd  
```
