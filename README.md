# Turbo UI

This project builds a GUI based tool for analysing linux turbostat output over a period of time. It also has a CLI script to achieve the same.

## Turbostat
Turbostat is an opensource tool for Linux. It reports processor topology, frequency, idle power-state statistics, temperature and power on X86 processors. The output of the tool is in a CSV format.

### Generating Turbostat output
To generate turbostat output
```
sudo turbostat -i .3 -q -o output.csv
```
- -i specifies the interval between every record
- -q for not outputing system information in the output. (**Note:** The input to the tool shouldn't have system information)
- -o specifiec the output file name

For generating only specific parameters, one can use the following command

```
sudo turbostat -i .3 -s Core,CPU,Avg_MHz,Busy%,Bzy_MHz,TSC_MHz,sysfs,IRQ,CoreTmp -q -o output.csv
```

## Tool Details
TurboUI has the following options in the GUI

1. **Select File Button**: Button to select the raw output file of turbostat
2. **Summary/CPU Button:** A toggle button where you can switch between CPU and summary views.
3. **Display Graph Button:** The button displays graph
4. **CPU List:** A multi select list where you can select multiple CPUs.
5. **Y Axis 1 Param List:** A single select list of turbostat columns which can be mapped to CPUs and will be drawn on left y axis. 
6. **Y Axis 2 Param List:** A single select list of turbostat columns which will draw the summary values on the right y axis.

## Execution
Follow the below steps to install requirements and launch the GUI tool

1. Clone the repository
2. Execute `pip install -r requirements.txt`
3. Execute `python index.py` to launch the GUI tool.
4. You can use `example/turbostat_out.csv` for testing the tool incase you don't have any turbostat output.

## Building
Use the following steps to build a executable out of this repository

1. Clone the repository
2. Install pyinstaller by executing `pip install pyinstaller`
3. Execute `pyinstaller --noconsole --onefile index.py`
4. This will generate a executable is the dist folder.

**Note:** To generate a executable for windows, the above command has to be executed on windows and same for linux and mac.

## CLI Script
The CLI tool to draw the graph is placed in `script` folder and named `turboscript.py`

It can be executed as follows
```
python turboscript.py [-h] [-s] [-y1 Y1PARAM] [-c [CPU]] [-y2 [Y2PARAM]] filename
```

Following are the arguments is takes
1. **-h / --help:** To see the arguments and what do they mean
2. **-s**: To draw summary graph with the params gives with -y1
3. **-y1 [Y1PARAM]:** Y1PARAM is a single parameter which should be the name of a column in raw turbostat output. This will be there on left y axis.
4. **-c [CPU]:** CPU is a command separated list of cpu numbers.
5. **-y2 [Y2PARAM]:** Y2PARAM is a summary parameter to be drawn on right y axis.
6. **filename:** This is a raw turbostat output

**Example Command**
```
python3 script/turboscript.py -y1 CoreTmp -c 0,6,7,1,2,3,4,5 example/turbostat_out.csv
```

