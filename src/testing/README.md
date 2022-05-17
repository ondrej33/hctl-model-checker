There are three types of automated tests:

1. Test whether evaluating attractor formula on several models results in expected (pre-computed) numbers of results:
    ```
    python3 test_attractors.py
    ```

2. Test whether evaluating coloured benchmark models and formulae result in expected (pre-computed) numbers of states:
    ```
    python3 test_benchmarks.py
    ```
    This may take some time to evaluate (~45 min).


3. Test whether the results of automatic parsing and evaluation match the results of manually evaluating formulae by components:
    ```
    python3 test_fixed_formulas.py model_file
    ```
    - `model_file` is a path (relative to project) to a file with BN model in bnet format (model should have 10-20 variables)
    
    Takes few seconds for models with ~10 variables; up to few minutes for models with 20+ variables.    


The following 3 concrete commands can be used to generally test the current state of the implementation:
```
python3 test_attractors.py
python3 test_benchmarks.py
python3 test_fixed_formulas.py 'benchmark_models/model_collection_large/[var:20]__[id:003]__[MAMMALIAN-CELL-CYCLE]/model_inputs_free.bnet'
```
