# HCTL_stuff

Základní implementace komponent pro model checking je v implementation.py. 
Je tam i ne úplně pěkná funkce, která zpracovává bnet formát do "modelu", pak pár funkcí pro vyhodnocování fixed formulí a nafouklá funkce na print výsledků.

Parser, gramatika pro HCTL a vše okolo je v Parsing_and_evaluation/. V parser_and_simulator.py je taková první verze celkového model checkeru, většina ostatních souborů je generovaná automaticky z gramatiky (nebo nějaké datové struktury).
