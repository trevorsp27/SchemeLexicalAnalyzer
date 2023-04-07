# Set -- Parse tree node strategy for printing the special form set!

from Tree import Nil
#from Tree import Unspecific
from Print import Printer
from Special import Special

class Set(Special):
    def __init__(self):
        pass
    
    def print(self, t, n, p):
        Printer.printSet(t, n, p)

    def eval(self, exp, env):
        args = exp.getCdr()
        id = args.getCar()
        value = args.getCdr().getCar().eval(env)
        env.assign(id, value)
        return Nil.getInstance()
