# HCTL_stuff

Základní implementace komponent pro model checking (EX, binder...) je v implementation.py. 
Je tam i celkem škaredá funkce, která zpracovává bnet formát do "modelu" +zatím uměle vytváří BDDčka, a pak nafouklá funkce na print výsledků.

Parser, gramatika pro HCTL a vše okolo je v Parsing_and_evaluation/. V parser_and_simulator.py je taková první verze celkového model checkeru (pár věcí dodělávám, zatím funguje jen pro "správně" formátované formulky), většina ostatních souborů ve folderu je generovaná automaticky z gramatiky (nebo jsou to nějaké datové struktury).

Zbytek jsou různé testy, helper scripty apod.
