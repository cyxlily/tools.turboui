import pandas as pd
import matplotlib.pyplot as plt

class Graph:
    @staticmethod
    def draw(dataTable, summaryTable, y1Param, cpus, isSummary, y2param):
        data = pd.DataFrame(dataTable)
        summary = pd.DataFrame(summaryTable)
        x = range(0,data.index.stop)
        fig, ax1 = plt.subplots(num= y1Param + " vs Instance", figsize=(10, 10))

        if isSummary:
            ax1.plot(x, [float(summary[y1Param][i][0]) for i in x], label="Summary")
        else:    
            for cpu in cpus:
                # Because cpus can be in random order as well
                index = data['CPU'][0].index(cpu.split(" ")[1])
                ax1.plot(x, [float(data[y1Param][i][index]) for i in x] , label=cpu)
        
        ax1.set_xlabel('Instances')
        ax1.set_ylabel(y1Param)

        if y2param != "None": 
            ax2 = ax1.twinx()

            ax2.plot(x, [float(summary[y2param][i][0]) for i in x], 'r:', label=y2param)
            ax2.set_ylabel(y2param)
            ax2.legend(loc='upper right')

        ax1.legend(loc='upper left')
        plt.show()