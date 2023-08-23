import pandas as pd
from PyQt5.QtWidgets import QMessageBox

class Parser:    
    @staticmethod    
    def parse_file(file_path):
        summary = []
        data = []
        with open(file_path) as f:
            lines = f.readlines()
        for i in range(len(lines)):
            line = lines[i].strip()
            if i==0 and not line.startswith('Core'):
                if line.startswith('cpu0: Guessing tjMax '):
                    continue
                else:
                    return 0
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
                    for j in range(len(values)):
                        table_summary_data[columns[j]] = table_data.get(columns[j], []) + [values[j]]
                for k in range(len(values)):
                    table_data[columns[k]] = table_data.get(columns[k], []) + [values[k]]
        return [data, summary]

