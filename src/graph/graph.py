import pandas as pd
import matplotlib.pyplot as plt

class Graph:
    @staticmethod
    def draw(dataTable, yParams, cpus, filename):
        data = pd.DataFrame(dataTable)
        x = range(0,data.index.stop)
        fig, ax1 = plt.subplots(figsize=(10, 10))
        yParam=yParams.pop(-1)
        endAs = yParam[-1]
        for cpu in cpus:
            # Because cpus can be in random order as well
            index = data['CPU'][0].index(cpu)
            ax1.plot(x, [float(data[yParam][i][index]) for i in x] , label=cpu + " " + yParam)
            for yParam in yParams:
                if yParam[-1] == endAs:
                    ax1.plot(x, [float(data[yParam][i][index]) for i in x] , label=cpu + " " + yParam)
                else:
                    ax2 = ax1.twinx()
                    ax2.plot(x, [float(data[yParam][i][0]) for i in x], 'r:', label=cpu + " " + yParam)
                    ax2.set_ylabel(yParam)
                    ax2.legend(loc='upper right')
                    print("Params end with different char, only display two Params.")
                    break

        
        ax1.set_xlabel('Time')

        plt.title(filename.split("/")[-1])
        ax1.legend(loc='upper left')
        plt.show()
