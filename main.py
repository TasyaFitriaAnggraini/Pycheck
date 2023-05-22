import lexerpycheck
import parserpycheck
import interpreterpycheck

from sys import *

lexer = lexerpycheck.lexerpycheck()
parser = parserpycheck.parserpycheck()
env = {}

file = open(argv[1])
text = file.readlines()

for line in text:
    tree = parser.parse(lexer.tokenize(line))
    interpreterpycheck.pycheckesekusi(tree, env)
