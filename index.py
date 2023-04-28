import sys
import pandas as pd
from PyQt5.QtWidgets import QMessageBox, QLabel, QApplication, QWidget, QVBoxLayout, QFileDialog, QPushButton, QComboBox, QHBoxLayout, QListWidget, QListWidgetItem
from qt_material import apply_stylesheet
from src.graph.graph import Graph
from src.parser.parser import Parser

class GraphApp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'TurboUI'
        self.width = 640
        self.height = 480
        self.initUI()
        self.showSummary = False

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, self.width, self.height)

        # Select file button
        self.select_file_btn = QPushButton('Select File', self)
        self.select_file_btn.clicked.connect(self.selectFile)

        # Summary button
        self.summary_btn = QPushButton('Summary', self)
        self.summary_btn.clicked.connect(self.changeOptions)
        self.summary_btn.setDisabled(True)

        # Display graph button
        self.display_graph_btn = QPushButton('Display Graph', self)
        self.display_graph_btn.clicked.connect(self.draw_graph)
        self.display_graph_btn.setDisabled(True)

        # CPU selection layout
        c_layout = QVBoxLayout()
        self.c_label = QLabel('CPU')
        self.cpuSelect = QListWidget()
        self.cpuSelect.setSelectionMode(QListWidget.MultiSelection)
        c_layout.addWidget(self.c_label)
        c_layout.addWidget(self.cpuSelect)

        # Y1 Parameter
        y1p_layout = QVBoxLayout()
        self.y1p_label = QLabel('Y1 Params')
        self.y1ParamSelect = QListWidget()
        y1p_layout.addWidget(self.y1p_label)
        y1p_layout.addWidget(self.y1ParamSelect)

        # Y2 Parameter
        y2p_layout = QVBoxLayout()
        self.y2p_label = QLabel('Y2 Params')
        self.y2ParamSelect = QListWidget()
        self.y2ParamSelect.setSelectionMode(QListWidget.SingleSelection)
        y2p_layout.addWidget(self.y2p_label)
        y2p_layout.addWidget(self.y2ParamSelect)

        # Buttons layout
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.select_file_btn)
        button_layout.addWidget(self.summary_btn)
        button_layout.addWidget(self.display_graph_btn)

        # Final layout
        layout = QHBoxLayout()
        layout.addLayout(button_layout)
        layout.addLayout(c_layout)
        layout.addLayout(y1p_layout)
        layout.addLayout(y2p_layout)
        self.setLayout(layout)

        extra = {
            'font_family': 'monoespace',
            'font_size': '26px',
            'density_scale': '1'
        }
        apply_stylesheet(self, theme='dark_cyan.xml', invert_secondary=True, extra=extra)


    def changeOptions(self):
        self.showSummary = not self.showSummary
        self.cpuSelect.clear()
        self.y1ParamSelect.clear()
        self.y2ParamSelect.clear()
        if self.showSummary:
            self.summary_btn.setText("CPUS")
            self.cpuSelect.setVisible(False)
            self.y2ParamSelect.setVisible(False)
            self.c_label.setVisible(False)
            self.y2p_label.setVisible(False)
            self.addSummaryOptions()
        else:
            self.summary_btn.setText("Summary")
            self.cpuSelect.setVisible(True)
            self.y2ParamSelect.setVisible(True)
            self.c_label.setVisible(True)
            self.y2p_label.setVisible(True)
            self.addCPUOptions()

    def selectFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select CSV File", "",
                                                   "CSV Files (*.csv)", options=options)
        if file_name:
            self.file_name = file_name
            self.parse_input_file()

    def parse_input_file(self):
        file_path = self.file_name
        parsedData = Parser.parse_file(file_path)
        if not parsedData:
            QMessageBox.critical(self, 'Error', 'Please select a valid input file')
            return
        self.data = parsedData[0]
        self.summary = parsedData[1]
        df = pd.DataFrame(self.data)
        dfSummary = pd.DataFrame(self.summary)
        self.df = df
        self.dfSummary = dfSummary
        if self.showSummary:
            self.changeOptions()
        self.cpuSelect.clear()
        self.y1ParamSelect.clear()
        self.y2ParamSelect.clear()
        self.addCPUOptions()
        self.showSummary = False
        self.summary_btn.setDisabled(False)
        self.display_graph_btn.setDisabled(False)

    def addCPUOptions(self):
        for item in self.df['CPU'][0]:
            self.cpuSelect.addItem(QListWidgetItem("CPU " + item))
        for item in self.df.columns:
            if item == 'Avg_MHz' or item== 'Busy%' or item=='Bzy_MHz' or item=='TSC_MHz':
                self.y1ParamSelect.addItem(QListWidgetItem(item))
        self.y2ParamSelect.addItem("None")
        self.y2ParamSelect.addItem("CoreTmp")
        self.y2ParamSelect.addItem("IRQ")
        self.y1Param = 'Avg_MHz'

    def addSummaryOptions(self):
        for item in self.dfSummary.columns:
            if item!='Core' and item!='CPU':
                self.y1ParamSelect.addItem(QListWidgetItem(item))
        self.y1Param = 'Avg_MHz'
    
    def draw_graph(self):
        if self.showSummary:
            if not self.y1ParamSelect.selectedItems():
                QMessageBox.critical(self, 'Error', 'Please select a Y1 Param')
                return
            self.y1Param = self.y1ParamSelect.selectedItems()[0].text()
            Graph.draw(self.data, self.summary, self.y1Param, ["Summary"], True, "None")
        else:   
            self.selected_cpus = []
            if not self.cpuSelect.selectedItems():
                QMessageBox.critical(self, 'Error', 'Please select atleast one CPU')
                return
            if not self.y1ParamSelect.selectedItems():
                QMessageBox.critical(self, 'Error', 'Please select a Y1 Param')
                return
            for cpu in self.cpuSelect.selectedItems():
                self.selected_cpus.append(cpu.text())

            self.y2Param = "None"
            if(len(self.y2ParamSelect.selectedItems()) > 0):  
                self.y2Param = self.y2ParamSelect.selectedItems()[0].text()    
            self.y1Param = self.y1ParamSelect.selectedItems()[0].text()
            Graph.draw(self.data, self.summary, self.y1Param, self.selected_cpus, False, self.y2Param)
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    graph_app = GraphApp()
    graph_app.show()
    sys.exit(app.exec_())

