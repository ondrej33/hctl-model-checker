#!/bin/bash

project_dir="."
models_dir="./benchmark_models/model_collection_large/"

for m in `ls ${models_dir}`
do
    if [ -f "${m}" ]; then
        # we only want directories containing models, this is probably a README file
        continue
    fi

    echo "-------------------------------"
    echo ${m}
    echo "-------------------------------"
    echo ''

    # there are two types of BN models in this collection - without inputs (fully specified) and with inputs
    # models with inputs have more files in their directory which we can use to distinguish them
    # for models with inputs we consider the version with all inputs fixed to 0

    if [ -f "${models_dir}/${m}/model_inputs_false.bnet" ]; then
        timeout -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model_inputs_false.bnet" 'AF !{x}: (AX (~{x} && AF {x}))'
        timeout -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model_inputs_false.bnet" 'AF !{x}: ((AX (~{x} && AF {x})) && (EF !{y}: EX ~AF {y}))'
        timeout -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model_inputs_false.bnet" '!{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y})'
        timeout -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model_inputs_false.bnet" '3{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y}) && EF ({x} && !{z}: AX {z}) && EF ({y} && !{z}: AX {z}) && AX (EF ({x} && !{z}: AX {z}) ^ EF ({y} && !{z}: AX {z}))'
    else
        timeout -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model.bnet" 'AF !{x}: (AX (~{x} && AF {x}))'
        timeout -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model.bnet" 'AF !{x}: ((AX (~{x} && AF {x})) && (EF !{y}: EX ~AF {y}))'
        timeout -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model.bnet" '!{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y})'
        timeout -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model.bnet" '3{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y}) && EF ({x} && !{z}: AX {z}) && EF ({y} && !{z}: AX {z}) && AX (EF ({x} && !{z}: AX {z}) ^ EF ({y} && !{z}: AX {z}))'
    fi
done
