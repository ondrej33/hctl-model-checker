#!/bin/bash

# first argument is number of model category to test (from 1 to 5)
# second argument is the type of test to make (binder, jump, exist, union_one, union_both)

path_beginning='/home/xhuvar/dd-stuff/bnet_example_files/'

# OK for paths on laptop
models_upto_10_vars="007 109 088 031 106 110 133 023 084 144"
# OK for paths on AISA
models_11_to_20_vars="100 058 057 015 091 089 026 074 090 099 107 140 055 139 003a 086"
# ideal testing for basics

# TODO
models_21_to_30_vars="024a 022a 069a 068a 103 045a 101 061 008a 105 142"
# OK for basics on laptop
models_31_to_60_vars="087 043 013 079 075 092 085"
# OK for basics on AISA
models_61_to_100_vars="093 051a 128a 056"
# migh be OK
models_101_plus_vars="138a 118a 039a"

# another added stuff 30-60, all having params
models_added="135a 065a 073a 129a 032a 020a 081a 060a 017a 076a 046a 070a 025a"

number_tests=9 # number of tests, longest tests are at the end (cant use for large sets)
models_to_test=""
if [ $1 = 1 ]; then
    models_to_test=$models_upto_10_vars
elif [ $1 = 2 ]; then
    models_to_test=$models_11_to_20_vars
    number_tests=7
elif [ $1 = 3 ]; then
    models_to_test=$models_21_to_30_vars
    number_tests=7
elif [ $1 = 4 ]; then
    models_to_test=$models_31_to_60_vars
    number_tests=7
elif [ $1 = 5 ]; then
    models_to_test=$models_61_to_100_vars
    number_tests=7
elif [ $1 = 6 ]; then
    models_to_test=$models_101_plus_vars
    number_tests=7
elif [ $1 = 7 ]; then
    models_to_test=$models_added
    number_tests=7
fi

for m in $models_to_test
do
    echo "-------------------------------"
    echo ${m}
    echo "-------------------------------"

    for ((i=0; i<=$number_tests; i++))
    do
	# usage: main2.py file_name test_name seq_num test_type
	python3 /home/xhuvar/dd-stuff/dd-0.5.6/dd/main2.py "${path_beginning}${m}.bnet" "$2" "$i" "n"
        python3 /home/xhuvar/dd-stuff/dd-0.5.6/dd/main2.py "${path_beginning}${m}.bnet" "$2" "$i" "o"
    done
done
