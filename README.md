# Symbolic HCTL Model Checker

This repository contains the implementation of the symbolic model checker for the logic HCTL.
It is focused on the analysis of (partially specified) Boolean networks. In particular, it allows to check for any behavioural hypotheses expressible in HCTL on large, non-trivial networks. This includes properties like stability, bi-stability, attractors, or oscillatory behaviour.

For given Boolean network (with inputs) and HCTL formula (representing the property we want to check), it computes all the states of the network (and corresponding colours) that satisfy the formula.
Depending on the mode, either prints the numbers of satisfying states and colours, or prints all the satisfying assignments.

The usage is following:
```
python3 src/model_check.py model_file hctl_formula [-p]
```

- `model_file` is a path to a file with BN model in bnet format (i.e. `benchmark_models/coloured_benchmarks/1.bnet`)
- `hctl_formula` is a valid HCTL formula in correct format
- Add `-p` for printing all ordered satisfying coloured states (might be infeasible)

For example, with concrete arguments, command might look like:
```
python3 src/model_check.py ./benchmark_models/coloured_benchmarks/1.bnet '!{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y})'
```


# Inputs and Models

The tool takes BN models in the `bnet` format as its input, with many example models present in the `benchmark_models` directory. Benchmark models are also present in the aeon formats, but this is just for the convenience of the user and those can't be used as inputs.

The grammar for HCTL is specified in the readable format in the file `src/parse_hctl_formula/HCTL.g4`. Example formulae can be found in the file `formulae_examples.txt`.


# Benchmarks

To run the benchmarks from the Evaluation, two bash scripts are prepared:

- `script_eval_coloured.sh` which model-checks all four presented formulas on six models from the `benchmark_models/coloured_benchmarks` directory
- `script_eval_monochromatic.sh` which model-checks all four formulas on 145 models from the `benchmark_models/models_collection_large` directory, with 1h timeout

Pre-computed results for the coloured set are available directly in the `benchmark_models/coloured_benchmarks` folder.
Results for the monochromatic set are available in the `benchmark_models/results_monochromatic` folder.


# Setup

Following steps should work on Linux systems (tested on Aisa and Psyche servers), as well as WSL. Creating Python virtual environment first is recommended.

Two main libraries are needed:
- [dd](https://github.com/tulip-control/dd) for the underlying binary decision diagrams implementation
- [ANTLR4](https://github.com/antlr/antlr4/blob/master/doc/python-target.md) for the parser of both HCTL formulae and update functions

To set up ANTLR and some other minor modules and requirements:
```
pip install wheel
pip install -r requirements.txt
```

To install the dd library's Cython bindings for CUDD:
```
pip download dd --no-deps  
tar xzf dd-*.tar.gz  
cd dd-*/  
python setup.py install --fetch --cudd  
```

If any problems occur during the installation, [dd](https://github.com/tulip-control/dd) page contains convenient instructions.


# Code Structure

The main script to run is the `model_check.py`.

The main body of the bottom-up model-checking algorithm, together with the caching and optimizations, is implemented in the `evaluator_hctl.py`.
The evaluation of individual HCTL operators (like EX, binder, ...) can be found in the `implementation_components.py`.
Encoding of the update functions of BN variables (to BDD representation) is handled in `evaluator_update_fn.py`.

In the `parse_hctl_formula` directory, there is a grammar and parser for the HCTL logic.
Most of the other files in the folder is generated automatically from the grammar by ANTLR.
Similarly, in the `parse_update_function` directory, there is a grammar and utilities for parsing the update functions of BN variables.

The file `parse_all.py` contains functions to transform the Boolean network model into its symbolic representation, and the HCTL formula to its syntax tree.
That includes (sort of) canonization of state variables in the formula.

In the `abstract_syntax_tree.py` and `model.py`, the main data structures can be found.

## Tests

Basic overall tests of the model-checking procedure are present in the `src/testing` folder, together with their instructions (readme).
