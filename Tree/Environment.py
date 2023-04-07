# Environment -- a data structure for Scheme environments

# An Environment is a list of frames.  Each frame represents a scope
# in the program and contains a set of name-value pairs.  The first
# frame in the environment represents the innermost scope.

# For the code below, I am assuming that a frame is implemented
# as an association list, i.e., a list of two-element lists.  E.g.,
# the association list ((x 1) (y 2)) associates the value 1 with x
# and the value 2 with y.

# To implement environments in an object-oriented style, it would
# be better to define a Frame class and make an Environment a list
# of such Frame objects or to implement a frame as a hash table.

# You need the following methods for modifying environments:
#  - constructors:
#      - create the empty environment (an environment with an empty frame)
#      - add an empty frame to the front of an existing environment
#  - lookup the value for a name (for implementing variable lookup)
#      if the name exists in the innermost scope, return the value
#      if it doesn't exist, look it up in the enclosing scope
#      if we don't find the name, it is an error
#  - define a name (for implementing define and parameter passing)
#      if the name already exists in the innermost scope, update the value
#      otherwise add a name-value pair as first element to the innermost scope
#  - assign to a name (for implementing set!)
#      if the name exists in the innermost scope, update the value
#      if it doesn't exist, perform the assignment in the enclosing scope
#      if we don't find the name, it is an error


import sys
import os.path
from Tree import Node
from Tree import IntLit
from Tree import StrLit
from Tree import Ident
from Tree import Nil
from Tree import Cons
from Tree import BuiltIn

class Environment(Node):
    # An Environment is implemented like a Cons node, in which
    # every list element (every frame) is an association list.
    # Instead of Nil(), we use None to terminate the list.

    def __init__(self, e = None):
        self.frame = Nil.getInstance()  # the innermost scope, an assoc list
        self.env = e                    # the enclosing environment

    def isEnvironment(self):
        return True

    def print(self, n, p=False):
        for _ in range(n):
            sys.stdout.write(' ')
        sys.stdout.write("#{Environment")
        if self.frame != None:
            self.frame.print(abs(n) + 4)
        if self.env != None:
            self.env.print(abs(n) + 4)
        for _ in range(abs(n)):
            sys.stdout.write(' ')
        sys.stdout.write(" }\n")
        sys.stdout.flush()

    @staticmethod
    def populateEnv(env, ini_file):
        lst = ["b+", "b-", "b*", "b/", "b=", "b<", "eq?", \
            "null?", "number?", "symbol?", "pair?", "procedure?", \
                "car", "cdr", "cons", "set-car!", "set-cdr!", \
                    "read", "write", "display", "newline", \
                        "eval", "apply", "interaction-environment", "load"]
        # print(lst)
        for name in lst:
            id = Ident(name)
            env.define(id, BuiltIn(id))
            # id.print(0)
            # BuiltIn(id).print(0)
            # sys.stdout.write("hi")
            id.eval(env)
        # env.print(0)
        exp = Cons(Ident("load"),(Cons(StrLit(ini_file), Nil.getInstance())))
        exp.eval(env)

        # BuiltIn((Ident("load")).apply(Cons(StrLit(ini_file), Nil.getInstance)))


    # This is not in an object-oriented style, it's more or less a
    # translation of the Scheme assq function.
    @staticmethod
    def __find(id, alist):
        if not alist.isPair():
            return None 	# in Scheme we'd return #f
        else:
            bind = alist.getCar()
            # bind.print(0)
            if id.getName() == bind.getCar().getName():
                # return a list containing the value
                return bind.getCdr()
            else:
                return Environment.__find(id, alist.getCdr())

    def lookup(self, id):
        val = Environment.__find(id, self.frame)
        # self.frame.print(0)
        # val.print(0)
        # self.env.print(0)
        if val == None and self.env == None:   
            self._error("undefined variable " + id.getName())
            return Nil.getInstance()         
        elif val == None:
            # look up the identifier in the enclosing scope
            return self.env.lookup(id)
        else:
            # get the value out of the list we got from find()
            return val.getCar()

    def define(self, id, value):
        val = Environment.__find(id, self.frame)
        if val == None:
            bind = Cons(id, Cons(value, Nil.getInstance()))
            self.frame = Cons(bind, self.frame)
        else:
            val.setCar(value)

    def assign(self, id, value):
        # Look up the variable in the assoc list and modifies its value
        val = Environment.__find(id, self.frame)
        if val == None and self.env == None:
            self._error("undefined variable " + id.getName())
        elif val == None:
            # look up the identifier in the enclosing scope
            self.env.assign(id, value)
        else:
            # change the value in the list we got from find()
            val.setCar(value)

    # Helper function for implementing Closure.
    # Does the same thing as define, but the input arguments are lists
    def defineList(self, l1, l2):
        # l1.print(0)
        # l2.print(0)
        if l1.isNull():
            pass
        elif not l1.isPair():
            # l2_quote = Cons(Ident("quote"), Cons(l2, Nil.getInstance()))
            self.define(l1, l2)
        elif l2.isNull():
            self.define(l1.getCar(), Nil.getInstance())
            self.defineList(l1.getCdr(), Nil.getInstance())
        else:
            self.define(l1.getCar(), l2.getCar())
            self.defineList(l1.getCdr(), l2.getCdr())

if __name__ == "__main__":
    env = Environment()
    env.define(Ident("foo"), IntLit(42))
    env.print(0)
