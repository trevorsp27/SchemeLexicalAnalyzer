# StLit -- Parse tree node class for representing string literals

import sys
from Tree import Node
from Print import Printer

class StrLit(Node):
    printDoubleQuotes = True

    @classmethod
    def setDoubleQuotes(cls, val):
        cls.printDoubleQuotes = val

    def __init__(self, s):
        self.strVal = s

    def print(self, n, p=False):
        if StrLit.printDoubleQuotes:
            Printer.printStrLit(n, self.strVal)
        else:
            for _ in range(n):
                sys.stdout.write(' ')
            sys.stdout.write(self.strVal)
            if n >= 0:
                sys.stdout.write('\n')
                sys.stdout.flush()

    def getStrVal(self):
        return self.strVal

    def isString(self):
        return True
    
    def eval(self,env):
        return self

if __name__ == "__main__":
    id = StrLit("foo")
    id.print(0)
