import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt

def parse_file(file_path):
    summary = []
    data = []
    with open(file_path) as f:
        lines = f.readlines()
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith('Core'):
            table_data = {}
            table_summary_data = {}
            columns = line.split()
        else: 
            if i+1 < len(lines) and lines[i+1].strip().startswith('Core'):
                data.append(table_data)
                summary.append(table_summary_data)
            values = line.split()
            if values[0].startswith('-'):
                for i in range(len(values)):
                    table_summary_data[columns[i]] = table_data.get(columns[i], []) + [values[i]]
                continue
            for i in range(len(values)):
                table_data[columns[i]] = table_data.get(columns[i], []) + [values[i]]
    return [data, summary]

def draw(dataTable, summaryTable, y1Param, cpus, isSummary, y2param):
    data = pd.DataFrame(dataTable)
    summary = pd.DataFrame(summaryTable)
    x = range(0,data.index.stop)
    fig, ax1 = plt.subplots(num= y1Param + " vs Instance", figsize=(10, 10))

    if isSummary:
        ax1.plot(x, [float(summary[y1Param][i][0]) for i in x], label="Summary")
    else:    
        for cpu in cpus:
            index = data['CPU'][0].index(cpu)
            ax1.plot(x, [float(data[y1Param][i][index]) for i in x] , label="CPU "+cpu)
    
    ax1.set_xlabel('Instances')
    ax1.set_ylabel(y1Param)

    if y2param and y2param != "None": 
        ax2 = ax1.twinx()

        ax2.plot(x, [float(summary[y2param][i][0]) for i in x], 'r:', label=y2param)
        ax2.set_ylabel(y2param)
        ax2.legend(loc='upper right')

    ax1.legend(loc='upper left')
    plt.show()

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--summary", help="(Optional) To draw summary graph", action="store_true")
parser.add_argument("-y1", "--y1param", help="The parameter to be plotted on left y axis", type=str)
parser.add_argument("-c", "--cpu", help="Comma separated CPU values", type=str, nargs='?', const='default', default="")
parser.add_argument("-y2", "--y2param", help="(Optional) The summary parameter to be plotted on right Y axis (CoreTmp, IRQ)", type=str, nargs='?', const='default', default="None")
parser.add_argument("filename", help="Input filename", type=str)

args = parser.parse_args()

parsedData = parse_file(args.filename)
data = parsedData[0]
summary = parsedData[1]
df = pd.DataFrame(data)
dfSummary = pd.DataFrame(summary)

if not args.summary and not args.cpu:
    print("Missing arguments, pls use --help to see the options")
    sys.exit()

draw(df, dfSummary, args.y1param, args.cpu.split(","), args.summary, args.y2param)
