# HCTL_stuff

V model.py se dá vybrat zvolením importu jestli chci python verzi dd knihovny, nebo cudd verzi (cudd je default, musí být ale stáhnutá).

Základní implementace komponent pro model checking (EX, binder...) je v implementation.py. 
V implementation.py jsou pak i funkce pro různá printování výsledků.

Parser, gramatika pro HCTL a vše okolo je v Parsing_HCTL_formula/. 
V HCTLVisitor.py je převod na abstract syntax tree, se kterým se pak dále pracuje.
V evaluator_hctl.py je pak pracovní verze celkového model checkeru (pár věcí dodělávám), včetně základních optimalizací.
Většina ostatních souborů ve folderu je generovaná automaticky z gramatiky nebo jsou to testy.

V Parsing_update_fns/ je pak podobná gramatika, parser a evaluator, ale tentokrát pro update funkce proměnných v booleovské síti.

Soubor parse_all.py pak obsahuje velkou funkci, která zastřešuje parsování booleovské sítě i formule, a vytváří strukturu modelu.
Navíc vrací už upravenou verzi stromu pro HCTL formuli (kanonizované formule apod).

Soubory abstract_syntax_tree.py a model.py pak obsahují hlavní datové struktury.

Zbytek jsou různé testy, helper scripty apod., nic moc důležitého.

Knihovny: https://github.com/tulip-control/dd, https://github.com/antlr/antlr4/blob/master/doc/python-target.md


========== SETUP: ==========  
DD + CUDD  
$ pip install cython

$ pip download dd --no-deps  
$ tar xzf dd-\*.tar.gz  
$ cd dd-\*/  
$ python setup.py install --fetch --cudd  
pak může být potřeba přidat do path (pythonpath) něco jako: $ export PYTHONPATH="${PYTHONPATH}:~/HCTL_stuff/venv/lib/python3.8/site-packages"


ANTLR pro generování z gramatiky (netřeba pro běžné používání)
$ cd /usr/local/lib  
$ wget https://www.antlr.org/download/antlr-4.9.2-complete.jar  
$ export CLASSPATH=".:/usr/local/lib/antlr-4.9.2-complete.jar:$CLASSPATH"  
$ alias antlr4='java -jar /usr/local/lib/antlr-4.9.2-complete.jar'  
$ alias grun='java org.antlr.v4.gui.TestRig'  

ANTLR pro runtime
$ pip install antlr4-python3-runtime

kroky wget a pip je někdy potřeba přes sudo

pak asi třeba přidat do pythonpath, něco jako: export PYTHONPATH="${PYTHONPATH}:/usr/local/lib/python3.8/dist-packages"

pak z gramatiky generuju soubory pomocí: $ antlr4 -Dlanguage=Python3 -visitor update_fn.g4  


TERMCOLOR  
$ pip install termcolor  


TIMEOUT DECORATOR  
$ pip install timeout-decorator
