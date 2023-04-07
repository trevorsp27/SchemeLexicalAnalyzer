# Regular -- Parse tree node strategy for printing regular lists

from Print import Printer
from Special import Special
import sys


class Regular(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printRegular(t, n, p)
        
    def eval(self, exp, env):
        from Tree import Nil
        call = Special.getUtil().mapeval(exp, env)
        fun = call.getCar()
        args = call.getCdr()
        if not fun.isProcedure():
            self._error(exp.getCar().getName() + " is not a procedure")
            return Nil.getInstance()
        return fun.apply(args)
        # sys.stdout.write("hi")

