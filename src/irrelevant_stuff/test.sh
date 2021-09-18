#!/bin/bash

model_numbers="029 095 064 097 063 067 010 053 104 035 036 037 021 028 062 049 003 024 119 096 131 022 069 040 047 068 042 045 033 034 038"
formulas="!{x}:(AX{x}) !{x}:(AG(EF{x})) !{x}:(EG(EF{x}))"

path_beginning='/home/xhuvar/HCTL_stuff/bnet_examples/'

for m in $model_numbers
do
    echo "-------------------------------"
    echo ${m}
    echo "-------------------------------"

    for f in formulas
    do
	      # usage: testing_full_eval.py file_name formula
	      python3 /home/xhuvar/HCTL_stuff/src/testing_full_eval.py "${path_beginning}${m}_free.bnet" "${f}"
    done
done
