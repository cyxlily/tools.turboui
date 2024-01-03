import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from src.parser.parser import Parser
from src.graph.graph import Graph

parser = argparse.ArgumentParser()
parser.add_argument("-y", "--yparam", help="The parameters to be plotted on y axis", type=str)
parser.add_argument("-c", "--cpu", help="Comma separated CPU values", type=str, nargs='?', const='default', default="")
parser.add_argument("filename", help="Input filename", type=str)

args = parser.parse_args()

parsedData = Parser.parse_file(args.filename)
data = parsedData[0]
df = pd.DataFrame(data)

if not args.yparam and not args.cpu:
    print("Missing arguments, pls use --help to see the options")
    sys.exit()

Graph.draw(df, args.yparam.split(","), args.cpu.split(","), args.filename)
