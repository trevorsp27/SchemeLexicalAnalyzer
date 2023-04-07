# Cond -- Parse tree node strategy for printing the special form cond

from Tree import BoolLit
from Tree import Nil
#from Tree import Unspecific
from Print import Printer
from Special import Special

class Cond(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printCond(t, n, p)
    
    @staticmethod
    def _eval(exp, env):
        test = exp.getCar().getCar()
        body = exp.getCar().getCdr()
        util = Special.getUtil()
        if test.getName() == "else":
            if body.isNull():
                return Nil.getInstance()
            else:
                return util.begin(body, env)
        else:
            val = test.eval(env)
            if val.getBoolVal():
                if body.isNull():
                    return val
                else:
                    return util.begin(body, env)
            else:
                return Cond._eval(exp.getCdr(), env)

    def eval(self, exp, env):
        return Cond._eval(exp.getCdr(), env)

