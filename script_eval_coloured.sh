#!/bin/bash

src_dir="./src"
models_dir="./benchmark_models/coloured_benchmarks"

for m in `ls ${models_dir}/*.bnet`
do
    echo "-------------------------------"
    echo ${m}
    echo "-------------------------------"
    echo ''

    python3 "${src_dir}/model_check.py" "${m}" 'AF !{x}: (AX (~{x} && AF {x}))'
    python3 "${src_dir}/model_check.py" "${m}" 'AF !{x}: ((AX (~{x} && AF {x})) && (EF !{y}: EX ~AF {y}))'
    python3 "${src_dir}/model_check.py" "${m}" '!{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y})'
    python3 "${src_dir}/model_check.py" "${m}" '3{x}: 3{y}: (@{x}: ~{y} && AX {x}) && (@{y}: AX {y}) && EF ({x} && !{z}: AX {z}) && EF ({y} && !{z}: AX {z}) && AX (EF ({x} && !{z}: AX {z}) ^ EF ({y} && !{z}: AX {z}))'
done
