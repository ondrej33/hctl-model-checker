grammar HCTL;

/** Main format structure **/

root : (NEWLINE+)? formula fullStop;

fullStop : NEWLINE+ | EOF ;

formula : value=PROP_NAME                                                      #terminalNode
        | value=VAR_NAME                                                       #terminalNode
        | value=(TRUE | FALSE)                                                 #terminalNode
        | value='(' child=formula ')'                                          #skipNode
        | value=NEG child=formula                                              #unary
        | value=TEMPORAL_UNARY child=formula                                   #unary
        // we list operators explicitly, becuase writing them as a subrule broke operator priority
        | left=formula value=CON right=formula                                 #binary
        | left=formula value=DIS right=formula                                 #binary
        | <assoc=right> left=formula value=IMPL right=formula                  #binary
        | left=formula value=EQIV right=formula                                #binary
        | left=formula value=E_U right=formula                                 #binary
        | left=formula value=A_U right=formula                                 #binary
        | <assoc=right> left=formula value=E_W right=formula                   #binary
        | <assoc=right> left=formula value=A_W right=formula                   #binary
        | value=BIND var=VAR_NAME ':' child=formula                            #hybrid
        | value=JUMP var=VAR_NAME ':' child=formula                            #hybrid
        | value=EXISTS var=VAR_NAME ':' child=formula                          #hybrid
        ;


/** Terminals **/

TRUE : ([tT]'rue' | 'tt');
FALSE : ([fF]'alse' | 'ff');


/** Logical operators **/

NEG : '~';
CON : '&&';
DIS : '||';
IMPL : '->';
EQIV : '<->';


/** Path quantifiers **/

A : 'A';
E : 'E';

PATH : (A|E);


/** Temporal operators **/

X : 'X';
Y : 'Y';
F : 'F';
G : 'G';

TEMPORAL_UNARY : PATH (Y|X|G|F);

E_U : 'EU';
A_U : 'AU';
E_W : 'EW';
A_W : 'AW';


/** Hybrid operators **/
BIND : '!';
JUMP : '@';
EXISTS: '3';


/** Propositions and variables **/
VAR_NAME: '{'[_a-zA-Z0-9]+'}';
PROP_NAME : [_a-zA-Z0-9]+;


/** Other stuff, skipping **/

NEWLINE : '\r'?'\n';

WS : [ \t]+ -> skip ;
Block_comment : '/*' (Block_comment|.)*? '*/' -> skip ; // nesting allow
/*
C_Line_comment : '//' ~('\n'|'\r')* -> skip ;
Python_Line_comment : '#' ~('\n'|'\r')* -> skip ;
*/
