There are three types of automated tests:

1. Test whether evaluating attractor formula on several models results in same (pre-computed) numbers of results as the [AEON](https://github.com/sybila/biodivine-aeon-py) tool, which specializes on attractor detection:
    ```
    python3 testing_attractors.py
    ```

2. Test whether evaluating coloured benchmarks models and formulae result in expected (pre-computed) number of states:
    ```
    python3 testing_automatic.py
    ```
    This may take some time to evaluate.


3. Test whether result of automatic parsing and evaluation matches the result of manually evaluating formula:
    ```
    python3 testing_automatic.py model_file
    ```
    - `model_file` is a path to a file with BN model in bnet format, should be sufficiently small model (10-20 variables)
    
    Takes few seconds for models with ~10 variables, upto few minutes for models with 20+ variables.    


Following 3 concrete commands can be used to generally test the current state of the implementation:
```
python3 testing_attractors.py
python3 testing_automatic.py
python3 testing_automatic.py 'benchmark_models/model_collection_large/[var:20]__[id:003]__[MAMMALIAN-CELL-CYCLE]/model_inputs_free.bnet'
```
