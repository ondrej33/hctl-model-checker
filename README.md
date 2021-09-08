# HCTL_stuff

Základní implementace komponent pro model checking (EX, binder...) je v implementation.py. 
Je tam i celkem škaredá funkce, která zpracovává bnet formát do struktury "modelu" + zatím celkem uměle vytváří BDDčka, a pak i nafouklá funkce na print výsledků.

Parser, gramatika pro HCTL a vše okolo je v Parsing_and_evaluation/. V parser_and_simulator.py je taková první verze celkového model checkeru (pár věcí dodělávám, zatím funguje jen pro "správně" formátované formulky), většina ostatních souborů ve folderu je generovaná automaticky z gramatiky (nebo jsou to nějaké datové struktury).

Zbytek jsou různé testy, helper scripty apod., nic moc důležitého.

Knihovny: https://github.com/tulip-control/dd, https://github.com/antlr/antlr4/blob/master/doc/python-target.md
