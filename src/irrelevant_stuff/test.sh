#!/bin/bash

#formulas='AF(!{x}:(AX((~{x})&&(AF{x})))) AF(!{x}:((AX((~{x})&&(AF{x})))&&(EF(!{y}:(EX(~AF{y})))))) !{x}:3{y}:((@{x}:(~{y})&&(AX{x}))&&(@{y}:(AX{y})))'

project_dir="/home/ohuvar/HCTL_stuff"
models_dir="${project_dir}/benchmark_models/non_parametrized"


for m in `ls ${models_dir}`
do
    echo "-------------------------------"
    echo ${m}
    echo "-------------------------------"
    echo ''

    # usage: testing_full_eval.py file_name formula

    python3 "${project_dir}/src/testing_full_eval.py" "${models_dir}/${m}/model_inputs_false.bnet" 'AF !{x}: (AX (~{x} && AF {x}))'
    python3 "${project_dir}/src/testing_full_eval.py" "${models_dir}/${m}/model_inputs_true.bnet"  'AF !{x}: (AX (~{x} && AF {x}))'

    python3 "${project_dir}/src/testing_full_eval.py" "${models_dir}/${m}/model_inputs_false.bnet" 'AF !{x}: ((AX (~{x} && AF {x})) && (EF !{y}: EX ~AF {y}))'
    python3 "${project_dir}/src/testing_full_eval.py" "${models_dir}/${m}/model_inputs_true.bnet" 'AF !{x}: ((AX (~{x} && AF {x})) && (EF !{y}: EX ~AF {y}))'

    python3 "${project_dir}/src/testing_full_eval.py" "${models_dir}/${m}/model_inputs_false.bnet" '!{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y})'
    python3 "${project_dir}/src/testing_full_eval.py" "${models_dir}/${m}/model_inputs_true.bnet" '!{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y})'

    python3 "${project_dir}/src/testing_full_eval.py" "${models_dir}/${m}/model_inputs_false.bnet" '3{x}: 3{y}: (@{x}: (~{y} && AX {x})) && (@{y}: (AX {y})) && (!{z}: (EF {x}) && (EF {y}) && (AX (EF {x} ^ EF {y})))'
    python3 "${project_dir}/src/testing_full_eval.py" "${models_dir}/${m}/model_inputs_true.bnet" '3{x}: 3{y}: (@{x}: (~{y} && AX {x})) && (@{y}: (AX {y})) && (!{z}: (EF {x}) && (EF {y}) && (AX (EF {x} ^ EF {y})))'

done

