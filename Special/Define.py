# Define -- Parse tree node strategy for printing the special form define

from Tree import Ident
from Tree import Nil
from Tree import Cons
#from Tree import Void
from Print import Printer
from Special import Special

class Define(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printDefine(t, n, p)

    # For variable definition, add a binding to the environment
    # For function definition, construct a lambda expression
    def eval(self, exp, env):
        id = exp.getCdr().getCar()
        if id.isSymbol():
            value = exp.getCdr().getCdr().getCar().eval(env)
            env.define(id, value)
        else:
            name = id.getCar()
            parm = id.getCdr()
            body = exp.getCdr().getCdr()
            value = Cons(Ident("lambda"),Cons(parm, body)).eval(env)
            env.define(name, value)
        return Nil.getInstance()

