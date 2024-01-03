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
sudo turbostat -i .3 -s Core,CPU,Avg_MHz,Busy%,Bzy_MHz,TSC_MHz,sysfs,IRQ,CoreTmp,PkgTmp,GFXMHz,PkgWatt,CorWatt,GFXWatt,RAMWatt -q -o output.csv
```

## Tool Details
TurboUI has the following options in the GUI

1. **Select File Button**: Button to select the raw output file of turbostat
3. **Display Graph Button:** The button displays graph
4. **CPU List:** A multi select list where you can select multiple CPUs.
5. **Y Axis Param List:** A multiple select list of turbostat columns which can be mapped to CPUs and will be drawn on y axis.

## Execution
Follow the below steps to install requirements and launch the GUI tool

1. Clone the repository
2. Install gui library pyqt using `sudo apt-get install python3-pyqt5`
3. Execute `pip install -r requirements.txt` to install python dependencies.
4. Execute `python3 turboui.py` to launch the GUI tool.
5. You can use `example/turbostat_out.csv` for testing the tool incase you don't have any turbostat output.

## Building
Use the following steps to build a executable out of this repository

1. Clone the repository
2. Install pyinstaller by executing `pip install pyinstaller`
3. Execute `pyinstaller --noconsole --onefile index.py`
4. This will generate a executable is the dist folder.

**Note:** To generate a executable for windows, the above command has to be executed on windows and same for linux and mac.

## CLI Script
The CLI tool to draw the graph is named `turboscript.py`

It can be executed as follows
```
python turboscript.py [-h] [-y YPARAM] [-c [CPU]] filename
```

Following are the arguments is takes
1. **-h / --help:** To see the arguments and what do they mean
2. **-y [YPARAM]:** YPARAM is multiple parameters which should be the name of columns in raw turbostat output. This will be there on y axis.
3. **-c [CPU]:** CPU is a command separated list of cpu numbers.
4. **filename:** This is a raw turbostat output

**Example Command**
```
python3 turboscript.py -y Bzy_MHz -c 0,1,2,3,4,5,6,7,- example/turbostat_out.csv
python3 turboscript.py -y PkgWatt,CorWatt,GFXWatt,RAMWatt -c - example/turbostat_out.csv
```

