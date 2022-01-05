#!/bin/bash

model_numbers="029 095 064 097 063 067 010 053 104 035 036 037 021 028 062 049 003 024 119 096 131 022 069 040 047 068 042 045 033 034 038 042 045 033 034 038 027 098 135 136 068 044 134"

formulas="!{x}:(AG(EF{x}))"

project_dir='/home/ohuvar/HCTL_stuff'

for m in $model_numbers
do
    #echo "-------------------------------"
    #echo ${m}
    echo "-------------------------------"

    for f in $formulas
    do
        # usage: testing_full_eval.py file_name formula
        python3 "${project_dir}/src/testing_full_eval.py" "${project_dir}/bnet_examples/${m}_free.bnet" "${f}"
    done
done
