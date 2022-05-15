There are three types of automated tests:

1. Test whether evaluating attractor formula on several models results in same (pre-computed) numbers of results as the [AEON](https://github.com/sybila/biodivine-aeon-py) tool, which specializes on attractor detection:
    ```
    python3 test_attractors.py
    ```

2. Test whether evaluating coloured benchmarks models and formulae result in expected (pre-computed) number of states:
    ```
    python3 test_benchmarks.py
    ```
    This may take some time to evaluate.


3. Test whether result of automatic parsing and evaluation matches the result of manually evaluating formula:
    ```
    python3 test_fixed_formulas.py model_file
    ```
    - `model_file` is a path (relative to project) to a file with BN model in bnet format, should be sufficiently sized model (10-20 variables)
    
    Takes few seconds for models with ~10 variables, upto few minutes for models with 20+ variables.    


The following 3 concrete commands can be used to generally test the current state of the implementation:
```
python3 test_attractors.py
python3 test_benchmarks.py
python3 test_fixed_formulas.py 'benchmark_models/model_collection_large/[var:20]__[id:003]__[MAMMALIAN-CELL-CYCLE]/model_inputs_free.bnet'
```
