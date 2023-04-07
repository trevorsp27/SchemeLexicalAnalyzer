# Begin -- Parse tree node strategy for printing the special form begin

from Tree import Nil
from Print import Printer
from Special import Special
import Util

class Begin(Special):
    def __init__(self):
        pass

    def print(self, t, n, p):
        Printer.printBegin(t, n, p)

    def eval(self, exp, env):
        util = Special.getUtil()
        args = exp.getCdr()
        if util.length(args) < 0:
            self._error("Input argument not a list")

        return util.begin(args, env)
