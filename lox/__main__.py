import os
import sys

if __package__ in (None, ""):
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lox.Lox import Lox


def main():
    lox = Lox()
    lox.run()


if __name__ == "__main__":
    main()
