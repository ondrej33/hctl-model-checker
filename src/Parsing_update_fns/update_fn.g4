grammar update_fn;

/** Main format structure **/

root : (NEWLINE+)? formula fullStop;

fullStop : NEWLINE+ | EOF ;

formula : value=PROP_NAME                                                      #terminalNode
        | value=(TRUE | FALSE)                                                 #terminalNode
        | value='(' child=formula ')'                                          #skipNode
        | value=NEG child=formula                                              #unary
        // we list operators explicitly, becuase writing them as a subrule broke operator priority
        | left=formula value=CON right=formula                                 #binary
        | left=formula value=DIS right=formula                                 #binary
        | <assoc=right> left=formula value=IMPL right=formula                  #binary
        | left=formula value=EQIV right=formula                                #binary
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


/** Propositions **/
PROP_NAME : [_a-zA-Z0-9]+;


/** Other stuff, skipping **/

NEWLINE : '\r'?'\n';

WS : [ \t]+ -> skip ;
Block_comment : '/*' (Block_comment|.)*? '*/' -> skip ; // nesting allow
/*
C_Line_comment : '//' ~('\n'|'\r')* -> skip ;
Python_Line_comment : '#' ~('\n'|'\r')* -> skip ;
*/
