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

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, self.width, self.height)

        # Select file button
        self.select_file_btn = QPushButton('Select File', self)
        self.select_file_btn.clicked.connect(self.selectFile)

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

        # Y Parameter
        yp_layout = QVBoxLayout()
        self.yp_label = QLabel('Y Params')
        self.yParamSelect = QListWidget()
        self.yParamSelect.setSelectionMode(QListWidget.MultiSelection)
        yp_layout.addWidget(self.yp_label)
        yp_layout.addWidget(self.yParamSelect)

        # Buttons layout
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.select_file_btn)
        button_layout.addWidget(self.display_graph_btn)

        # Final layout
        layout = QHBoxLayout()
        layout.addLayout(button_layout)
        layout.addLayout(c_layout)
        layout.addLayout(yp_layout)
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
        self.yParamSelect.clear()
        self.cpuSelect.setVisible(True)
        self.c_label.setVisible(True)
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
        df = pd.DataFrame(self.data)
        self.df = df
        self.cpuSelect.clear()
        self.yParamSelect.clear()
        self.addCPUOptions()
        self.display_graph_btn.setDisabled(False)

    def addCPUOptions(self):
        for item in self.df['CPU'][0]:
            self.cpuSelect.addItem(QListWidgetItem(item))
        for item in self.df.columns:
            if item != 'Core' and item!= 'CPU':
                self.yParamSelect.addItem(QListWidgetItem(item))
    
    def draw_graph(self):
        self.selected_cpus = []
        self.yParams = []
        if not self.cpuSelect.selectedItems():
            QMessageBox.critical(self, 'Error', 'Please select at least one CPU')
            return
        if not self.yParamSelect.selectedItems():
            QMessageBox.critical(self, 'Error', 'Please select at least one Y Param')
            return
        for cpu in self.cpuSelect.selectedItems():
            self.selected_cpus.append(cpu.text())
        for yParam in self.yParamSelect.selectedItems():
            self.yParams.append(yParam.text())
        Graph.draw(self.data, self.yParams, self.selected_cpus, self.file_name)
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    graph_app = GraphApp()
    graph_app.show()
    sys.exit(app.exec_())
