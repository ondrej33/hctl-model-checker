from fixed_formulas_eval import *
from parser_and_simulator import parse_and_eval


def run_tests(model: Model):
    assert model_check_fixed1_v2(model) == parse_and_eval("!{x}: EX {x}", model)
    assert model_check_fixed2_v3(model) == parse_and_eval("!{x}: (AX {x})", model)
    assert model_check_fixed3(model) == parse_and_eval("!{x}: (EX (~{x} && (EX {x})))", model)
    assert model_check_fixed4(model) == parse_and_eval("!{x}: (EX (EF {x}))", model)
    assert model_check_fixed5(model) == parse_and_eval("!{x}: ((EX (EF {x})) && (EG s__3))", model)
    assert model_check_fixed6(model) == parse_and_eval("EF !{x}: (EF ((~s__0) && EF (s__0 && {x}) ) )", model)
    assert model_check_fixed7(model) == parse_and_eval("(EG s__2) && (EF ~s__0)", model)
    assert model_check_fixed8(model) == parse_and_eval("!{x}: EX ( ~{x} && (!{y}: EX {y}) )", model)
    assert model_check_fixed9(model) == parse_and_eval("!{x}: (AG EF {x})", model)
    assert model_check_fixed10_v2(model) == parse_and_eval("!{x}: EX ( ~{x} && (!{y}: AX {y}))", model)
    assert model_check_fixed11(model) == parse_and_eval("!{x}: EX ( !{y}: AX ({y} && ~{x}))", model)
    assert model_check_fixed12(model) == parse_and_eval("!{x}: ( Q{y}: ( {x} && EX {y} ) )", model)
    assert model_check_fixed13(model) == parse_and_eval("!{x}: (Q{y}: ({x} && AX ({y} && AX {y})))", model)
    assert model_check_fixed14(model) == parse_and_eval("!{x}: (Q{y}:({x} && EX (~{x} && {y} && AX {y})))", model)


if __name__ == '__main__':
    # TODO add path
    path_to_bnet = ""
    m = bnet_parser(path_to_bnet)
    run_tests(m)
