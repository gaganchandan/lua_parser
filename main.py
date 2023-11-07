from parser import parser
import sys

program = open(sys.argv[1], 'r').read()
parser.parse(program)
print("The program is syntactically correct")
