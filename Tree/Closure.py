# Closure -- the data structure for function closures

# Class Closure is used to represent the value of lambda expressions.
# It consists of the lambda expression itself, together with the
# environment in which the lambda expression was evaluated.

# The method apply() takes the environment out of the closure,
# adds a new frame for the function call, defines bindings for the
# parameters with the argument values in the new frame, and evaluates
# the function body.

import sys
from Tree import Node
from Tree import StrLit
from Tree import Nil
from Tree import Cons
from Tree import Environment
from Special import Special

class Closure(Node):
    util = None

    @classmethod
    def setUtil(cls, u):
        cls.util = u

    def __init__(self, f, e):
        self.fun = f                    # a lambda expression
        self.env = e                    # the environment in which
                                        # the function was defined

    def getFun(self):
        return self.fun

    def getEnv(self):
        return self.env

    def isProcedure(self):
        return True

    def print(self, n, p=False):
        for _ in range(n):
            sys.stdout.write(' ')
        sys.stdout.write("#{Procedure")
        if self.fun != None:
            self.fun.print(abs(n) + 4)
        for _ in range(abs(n)):
            sys.stdout.write(' ')
        sys.stdout.write(" }\n")
        sys.stdout.flush()
    
    # Helper function pairing up parameters and arguments
    @staticmethod
    def pairUp(l1, l2):
        if l1.isNull():
            return Nil.getInstance()
        elif l2.isNull():
            pair = Cons(l1.getCar(), Cons(Nil.getInstance(), Nil.getInstance()))
            return Cons(pair, Closure.pairUp(l1.getCdr(), Nil.getInstance()))
        else:
            pair = Cons(l1.getCar(), Cons(l2.getCar(), Nil.getInstance()))
            return Cons(pair, Closure.pairUp(l1.getCdr(), l2.getCdr()))


    # pair up the input arguments with the lambda parameters,
    # then unpack the body and evaluate it
    def apply(self, args):
        parm = self.fun.getCdr().getCar()
        body = self.fun.getCdr().getCdr()
        # parm.print(0)
        # args.print(0)
        newEnv = Environment(self.env)
        newEnv.defineList(parm, args)
        # newEnv.print(0)
        return Special.getUtil().begin(body, newEnv)
        
