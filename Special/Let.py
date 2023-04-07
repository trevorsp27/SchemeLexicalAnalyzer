# Let -- Parse tree node strategy for printing the special form let

from Tree import Nil
from Tree import Cons
from Tree import Environment
from Print import Printer
from Special import Special

class Let(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printLet(t, n, p)

    # Evaluate the bindings in the given list, 
    # and add to the Environment
    @staticmethod
    def letEnv(lst, env):
        if lst.isNull():
            return env
        else:
            bind = lst.getCar()
            id = bind.getCar()
            value = bind.getCdr().getCar().eval(env)
            env.define(id, value)
            return Let.letEnv(lst.getCdr(), env)
    
    # Put a new scope in front of the environment,
    # Evaluate the let-bindings,
    # then evaluate the body
    def eval(self, exp, env):
        from Util import Util
        newEnv = Let.letEnv(exp.getCdr().getCar(), Environment(env))
        return Special.getUtil().begin(exp.getCdr().getCdr(), newEnv)
        