from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QComboBox,
    QLabel,
    QFileDialog,
    QLineEdit
)


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("app")

        app_layout = QVBoxLayout()
        file_path_layout = QHBoxLayout()
        output_layout = QHBoxLayout()
        input_layout = QHBoxLayout()
    
        self.selected_file = ""
        file_button = QPushButton("Select File")
        file_button.clicked.connect(self.openFileDialog)
        file_path_layout.addWidget(QLabel("Path to PDF file"))
        file_path_layout.addWidget(file_button)
        app_layout.addLayout(file_path_layout)

        output_layout.addWidget(QLabel("Output Filename"))
        self.output_filename = QLineEdit() 
        output_layout.addWidget(self.output_filename)
        app_layout.addLayout(output_layout)


        labels = ["Left margin", "Right margin", "Top margin", "Bottom margin"]
        margins = [QSpinBox() for _ in range(0, 4)]
        self.lmargin, self.rmargin, self.tmargin, self.bmargin = margins
        for label, margin in zip(labels, margins):
            input_layout.addWidget(QLabel(label))
            input_layout.addWidget(margin)


        units = ["px", "in", "cm", "mm"]
        self.unit = QComboBox()
        self.unit.addItems(units)
        input_layout.addWidget(QLabel("Units"))
        input_layout.addWidget(self.unit)

        app_layout.addLayout(input_layout)

        self.button = QPushButton("Add margin(s)")
        app_layout.addWidget(self.button)

        widget = QWidget()
        widget.setLayout(app_layout)
        self.setCentralWidget(widget)

    def openFileDialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Select File")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            self.selected_file = file_dialog.selectedFiles()[0]

