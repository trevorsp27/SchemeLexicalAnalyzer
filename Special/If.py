# If -- Parse tree node strategy for printing the special form if

from Tree import BoolLit
from Tree import Nil
#from Tree import Unspecific
from Print import Printer
from Special import Special

class If(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printIf(t, n, p)

    def eval(self, exp, env):
        args = exp.getCdr()
        if args.getCar().eval(env).getBoolVal():
            return args.getCdr().getCar().eval(env)
        else:
            return args.getCdr().getCdr().getCar().eval(env)
