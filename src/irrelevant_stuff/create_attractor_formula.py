data = "~ARF & AUXIAA & ~AUXIN & ~JKD & ~MGP & ~PLT & ~SCR & ~SHR & ~WOX5\n" + \
"~ARF & AUXIAA & ~AUXIN & ~JKD & ~MGP & ~PLT & ~SCR & SHR & ~WOX5\n" + \
"~ARF & AUXIAA & ~AUXIN & JKD & MGP & ~PLT & SCR & SHR & ~WOX5\n" + \
"ARF & ~AUXIAA & AUXIN & ~JKD & ~MGP & PLT & ~SCR & ~SHR & ~WOX5\n" + \
"ARF & ~AUXIAA & AUXIN & ~JKD & ~MGP & PLT & ~SCR & SHR & ~WOX5\n" + \
"ARF & ~AUXIAA & AUXIN & JKD & ~MGP & PLT & SCR & SHR & WOX5\n" + \
"ARF & ~AUXIAA & AUXIN & JKD & MGP & PLT & SCR & SHR & ~WOX5"

formula = ""
for item in data.split('\n'):
    if not item:
        break
    formula = formula + "(3{x}: ( @{x}: " + item + " & (!{y}: AG EF ({y} & " + item + " ) ) ) )" + " & "

formula = formula + "True"

"""
formula = formula + "~(3{x}:(@{x}: "
for item in data.split('\n'):
    formula = formula + "~(AG EF ( " + item + ")) " + " & "
formula = formula + "(!{y}: AG EF {y})))"
"""

print(formula)
 
