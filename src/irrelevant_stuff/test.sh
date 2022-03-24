#!/bin/bash

project_dir="/home/ohuvar/HCTL_stuff"
models_dir="/home/ohuvar/sysbio/biodivine-boolean-models/models/"

for m in `ls ${models_dir}`
do
    echo "-------------------------------"
    echo ${m}
    echo "-------------------------------"
    echo ''

    # usage: model_check.py file_name formula

    timeout -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model_inputs_false.bnet" 'AF !{x}: (AX (~{x} && AF {x}))'
    timeout -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model_inputs_true.bnet"  'AF !{x}: (AX (~{x} && AF {x}))'

    timeout -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model_inputs_false.bnet" 'AF !{x}: ((AX (~{x} && AF {x})) && (EF !{y}: EX ~AF {y}))'
    timeout -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model_inputs_true.bnet" 'AF !{x}: ((AX (~{x} && AF {x})) && (EF !{y}: EX ~AF {y}))'

    timeout -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model_inputs_false.bnet" '!{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y})'
    timeout -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model_inputs_true.bnet" '!{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y})'

    timeout -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model_inputs_false.bnet" '3{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y}) && EF ({x} && !{z}: AX {z}) && EF ({y} && !{z}: AX {z}) && AX (EF ({x} && !{z}: AX {z}) ^ EF ({y} && !{z}: AX {z}))'
    timeout -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model_inputs_true.bnet" '3{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y}) && EF ({x} && !{z}: AX {z}) && EF ({y} && !{z}: AX {z}) && AX (EF ({x} && !{z}: AX {z}) ^ EF ({y} && !{z}: AX {z}))'

    # timeout  -v 1h python3 "${project_dir}/src/model_check.py" "${models_dir}/${m}/model.bnet" 'AF !{x}: ((AX (~{x} && AF {x})) && (EF !{y}: EX ~AF {y}))'
done

