# Symbolic HCTL Model Checker

This repository contains the Python implementation of the symbolic model checker for the logic HCTL.
It is focused on the analysis of (partially specified) Boolean networks. In particular, it allows to check for any behavioural hypotheses expressible in HCTL on large, non-trivial networks. 
This includes properties like stability, bi-stability, attractors, or oscillatory behaviour.
You can find detailed information on the algorithm in [this thesis](https://is.muni.cz/th/zrf3h/).

For a given Boolean network (with inputs) and HCTL formula (representing the property we want to check), it computes all the states of the network (and corresponding colours) that satisfy the formula.
Depending on the mode, either prints the numbers of satisfying states and colours, or prints all the satisfying assignments.

Program invocation:
```
python3 src/model_check.py model_file hctl_formula [-p]
```

- `model_file` is a path to a file with BN model in bnet format (i.e. `./benchmark_models/coloured_benchmarks/1.bnet`)
- `hctl_formula` is a valid HCTL formula in correct format
- Add `-p` for printing all ordered satisfying coloured states (might be infeasible)

For example, with concrete arguments, commands illustrating the two modes might look like:
```
python3 src/model_check.py './benchmark_models/coloured_benchmarks/1.bnet' '!{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y})'
python3 src/model_check.py './benchmark_models/model_collection_large/[var-11]__[id-095]__[FISSION-YEAST-2008]/model_inputs_free.bnet' '!{x}: AX {x}' -p
```


# Setup

Following steps should work on usual Linux systems (tested on Adonis, Hedron and Psyche servers), as well as on WSL (Ubuntu). Python 3.8 or newer should be installed.

Two main libraries are needed:
- [dd](https://github.com/tulip-control/dd) for the underlying binary decision diagrams implementation
- [ANTLR4](https://github.com/antlr/antlr4/blob/master/doc/python-target.md) for the parser of both HCTL formulae and update functions

Creating Python virtual environment first is recommended, otherwise a problem with setuptools might arise.
```
python3 -m venv env
source env/bin/activate
```

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
python3 setup.py install --fetch --cudd  
```

If any problems occur during the installation, [dd](https://github.com/tulip-control/dd) page contains convenient instructions.


# Inputs and Models

The tool takes BN models in `bnet` format as its input, with many example models present in the `benchmark_models` directory. 
Benchmark models are also present in the aeon formats, but this is just for the convenience of the user (easier to visualise), and those can't be used as inputs.

The grammar for HCTL is specified in the readable format in the file `src/parse_hctl_formula/HCTL.g4`. 
Example formulae (including the four used for benchmarking) can be found in the file `formulae_examples.txt`.


# Benchmarks

To run the benchmarks from the Evaluation, you can run one of the two prepared bash scripts:

```
bash script_eval_coloured.sh
bash script_eval_monochromatic.sh
```
- `script_eval_coloured.sh` checks all four presented formulae on six models from the `benchmark_models/coloured_benchmarks` directory (takes ~45 min)

- `script_eval_monochromatic.sh` checks all four formulae on 145 models from the `benchmark_models/models_collection_large` directory, with 1h timeout for each run

Pre-computed results for the coloured set are available directly in the `benchmark_models/coloured_benchmarks` folder.
Results for the monochromatic set are available in the `benchmark_models/results_monochromatic` folder.


# Code Structure

The main script to run is the `model_check.py`.

The main body of the bottom-up model checking algorithm, together with the caching and optimizations, is implemented in `evaluator_hctl.py`.
The evaluation of individual HCTL operators (like EX, binder, ...) can be found in the `implementation_components.py`.
Encoding of the update functions of BN variables (to BDD representation) is handled in `evaluator_update_fn.py`.

In the `parse_hctl_formula` directory, there is a grammar and low-level parser for the HCTL logic.
Most of the other files in the folder were generated automatically from the grammar by ANTLR.
Similarly, in the `parse_update_function` directory, there is a grammar and utilities for low-level parsing of BN update functions.

The file `parse_all.py` wraps the functionality for transforming the Boolean network model into its symbolic representation, and the HCTL formula to its syntax tree.
That includes (sort of) canonization of state variables in the formula.

In the `abstract_syntax_tree.py` and `model.py`, two main data structures can be found.

## Tests

Basic overall tests of the model checking procedure are present in the `src/testing` folder, together with their specific instructions (readme).
