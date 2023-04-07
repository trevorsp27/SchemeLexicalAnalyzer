# BuiltIn -- the data structure for built-in functions

# Class BuiltIn is used for representing the value of built-in functions
# such as +.  Populate the initial environment with
# (name, BuiltIn(name)) pairs.

# The object-oriented style for implementing built-in functions would be
# to include the Python methods for implementing a Scheme built-in in the
# BuiltIn object.  This could be done by writing one subclass of class
# BuiltIn for each built-in function and implementing the method apply
# appropriately.  This requires a large number of classes, though.
# Another alternative is to program BuiltIn.apply() in a functional
# style by writing a large if-then-else chain that tests the name of
# the function symbol.

import sys
from Parse import *
from Tree import Node
from Tree import BoolLit
from Tree import IntLit
from Tree import StrLit
from Tree import Ident
from Tree import Nil
from Tree import Cons
from Tree import TreeBuilder
#from Tree import Unspecific

class BuiltIn(Node):
    env = None
    util = None

    @classmethod
    def setEnv(cls, e):
        cls.env = e

    @classmethod
    def setUtil(cls, u):
        cls.util = u

    def __init__(self, s):
        self.symbol = s                 # the Ident for the built-in function

    def getSymbol(self):
        return self.symbol

    def isProcedure(self):
        return True

    def print(self, n, p=False):
        for _ in range(n):
            sys.stdout.write(' ')
        sys.stdout.write("#{Built-In Procedure ")
        if self.symbol != None:
            self.symbol.print(-abs(n) - 1)
        sys.stdout.write('}')
        if n >= 0:
            sys.stdout.write('\n')
            sys.stdout.flush()


    # TODO: The method apply() should be defined in class Node
    # to report an error.  It should be overridden only in classes
    # BuiltIn and Closure.
    def apply(self, args):
        

        ## The easiest way to implement BuiltIn.apply is as an
        ## if-then-else chain testing for the different names of
        ## the built-in functions.  E.g., here's how load could
        ## be implemented:

        name = self.symbol.getName()
        # args.print(0)

        len = self.util.length(args)

        if len < 0:
            self._error("Input argument is not a list")

        # Functions with no argument
        elif len == 0:
            if name == "newline":
                sys.stdout.write("\n")
                return Nil.getInstance()
            elif name == "interaction-environment":
                return self.env
            elif name == "read":
                stream = sys.stdin.read()
                scanner = Scanner(stream)
                builder = TreeBuilder()
                parser = Parser(scanner, builder)
                return parser.parseExp()
            else:
                self._error("Procedure " + self.getSymbol().getName() + " does not have 0 argument")
                return Nil.getInstance()

        # Functions with one argument
        elif len == 1:
            arg1 = args.getCar()
            # arg1.print(0)
            if name == "eval":
                return arg1.eval(self.env)
            elif name == "symbol?":
                return BoolLit.getInstance(arg1.isSymbol())
            elif name == "number?":
                return BoolLit.getInstance(arg1.isNumber())
            elif name == "procedure?":
                return BoolLit.getInstance(arg1.isProcedure())
            elif name == "null?":
                return BoolLit.getInstance(arg1.isNull())
            elif name == "pair?":
                return BoolLit.getInstance(arg1.isPair())
            elif name == "car":
                return arg1.getCar()
            elif name == "cdr":
                return arg1.getCdr()
            elif name == "load":
                if not arg1.isString():
                    self._error("wrong type of argument")
                    return Nil.getInstance()
                filename = arg1.getStrVal()
                try:
                    scanner = Scanner(open(filename))
                    builder = TreeBuilder()
                    parser = Parser(scanner, builder)

                    root = parser.parseExp()
                    while root != None:
                        root.eval(BuiltIn.env)
                        root = parser.parseExp()
                except IOError:
                    self._error("could not find file " + filename)
                return Nil.getInstance()  # or Unspecific.getInstance()
            elif name == "write":
                arg1.print(0)
                return Nil.getInstance()
            elif name == "display":
                StrLit.setDoubleQuotes(False)
                arg1.print(0)
                StrLit.setDoubleQuotes(True)
                return Nil.getInstance()
            else:
                self._error("Procedure " + self.getSymbol().getName() + " does not take 1 argument")
                return Nil.getInstance()


        # Functions with 2 arguments
        elif len == 2:
            arg1 = args.getCar()
            arg2 = args.getCdr().getCar()
            if name == "apply":
                return arg1.apply(arg2)
            elif name == "eval":
                return arg1.eval(arg2)
            elif name == "b+":
                if not (arg1.isNumber() and arg2.isNumber()):
                    self._error("wrong type of argument")
                    return Nil.getInstance()
                else:
                    return IntLit(arg1.getIntVal() + arg2.getIntVal())
            elif name == "b-":
                if not (arg1.isNumber() and arg2.isNumber()):
                    self._error("wrong type of argument")
                    return Nil.getInstance()
                else:
                    return IntLit(arg1.getIntVal() - arg2.getIntVal())
            elif name == "b*":                
                if not (arg1.isNumber() and arg2.isNumber()):
                    self._error("wrong type of argument")
                    return Nil.getInstance()
                else:
                    return IntLit(arg1.getIntVal() * arg2.getIntVal())
            elif name == "b/":
                if not (arg1.isNumber() and arg2.isNumber()):
                    self._error("wrong type of argument")
                    return Nil.getInstance()
                elif arg2.getIntVal() == 0:
                    self.__error("Division by zero")
                    return Nil.getInstance()
                else:
                    return IntLit(arg1.getIntVal() / arg2.getIntVal())
            elif name == "b=":
                if not (arg1.isNumber() and arg2.isNumber()):
                    self._error("wrong type of argument")
                    return Nil.getInstance()
                else:
                    return BoolLit.getInstance(arg1.getIntVal() == arg2.getIntVal())
            elif name == "b<":
                if not (arg1.isNumber() and arg2.isNumber()):
                    self._error("wrong type of argument")
                    return Nil.getInstance()
                else:
                    return BoolLit.getInstance(arg1.getIntVal() < arg2.getIntVal())
            elif name == "eq?":
                if (arg1.isSymbol() and arg2.isSymbol()):
                    return BoolLit.getInstance(arg1.getName() == arg2.getName())
                else:
                    return BoolLit.getInstance(arg1 == arg2)
            elif name == "cons":
                return Cons(arg1, arg2)
            elif name == "set-car!":
                arg1.setCar(arg2)
                return Nil.getInstance()
            elif name == "set-cdr!":
                arg1.setCdr(arg2)
                return Nil.getInstance()
            else:
                self._error("Procedure " + name + "does not take 2 arguments")
                return Nil.getInstance()
        else:
            self._error("Procedure " + name + " does not take more than 2 arguments")

