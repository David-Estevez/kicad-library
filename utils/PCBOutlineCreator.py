from PySide import QtCore,QtGui
from PySide import QtUiTools
import os, sys
from kicad_board import KicadBoard

def load_ui(file_name, where=None):
    """
    Loads a .UI file into the corresponding Qt Python object
    :param file_name: UI file path
    :param where: Use this parameter to load the UI into an existing class (i.e. to override methods)
    :return: loaded UI
    """
    # Create a QtLoader
    loader = QtUiTools.QUiLoader()

    # Open the UI file
    ui_file = QtCore.QFile(file_name)
    ui_file.open(QtCore.QFile.ReadOnly)

    # Load the contents of the file
    ui = loader.load(ui_file, where)

    # Close the file
    ui_file.close()

    return ui

class PCBOutlineCreator(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUI()
        self.resetValues()


    def setupUI(self):
        # Load UI and set it as main layout
        ui_file_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'PCBOutlineCreator.ui')
        main_widget = load_ui(ui_file_path, self)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(main_widget)
        self.setLayout(layout)


        # Get a reference to all required widgets
        self.inputFileButton = self.findChild(QtGui.QToolButton, 'inputFileButton')
        self.inputFileLineEdit = self.findChild(QtGui.QLineEdit, 'inputFileLineEdit')
        self.exportButton = self.findChild(QtGui.QPushButton, 'exportButton')
        self.saveButton = self.findChild(QtGui.QPushButton, 'saveButton')
        self.lengthSpinBox = self.findChild(QtGui.QDoubleSpinBox, 'lengthSpinBox')
        self.widthSpinBox = self.findChild(QtGui.QDoubleSpinBox, 'widthSpinBox')
        self.lineWidthSpinBox = self.findChild(QtGui.QDoubleSpinBox, 'lineWidthSpinBox')
        self.cornersSpinBox = self.findChild(QtGui.QDoubleSpinBox, 'cornersSpinBox')
        self.cornersCheckBox = self.findChild(QtGui.QCheckBox, 'cornersCheckBox')
        self.xSpinBox = self.findChild(QtGui.QDoubleSpinBox, 'xSpinBox')
        self.ySpinBox = self.findChild(QtGui.QDoubleSpinBox, 'ySpinBox')

        # Configure widget ranges:
        max_float = sys.float_info.max
        self.lengthSpinBox.setMinimum(0)
        self.lengthSpinBox.setMaximum(max_float)
        self.widthSpinBox.setMinimum(0)
        self.widthSpinBox.setMaximum(max_float)
        self.lineWidthSpinBox.setMinimum(0)
        self.lineWidthSpinBox.setMaximum(max_float)
        self.lineWidthSpinBox.setSingleStep(0.1)
        self.cornersSpinBox.setMinimum(0)
        self.cornersSpinBox.setMaximum(max_float)
        self.xSpinBox.setMinimum(-max_float)
        self.xSpinBox.setMaximum(max_float)
        self.ySpinBox.setMinimum(-max_float)
        self.ySpinBox.setMaximum(max_float)

        # Connect slots/callbacks and signals
        self.cornersSpinBox.setEnabled(False)
        self.cornersCheckBox.stateChanged.connect(self.onCornersCheckBoxChangedState)
        self.saveButton.clicked.connect(self.onSaveButtonClicked)
        self.inputFileButton.clicked.connect(self.onInputFileButtonClicked)
        self.exportButton.clicked.connect(self.onExportButtonClicked)


    def resetValues(self):
        self.lengthSpinBox.setValue(50)
        self.widthSpinBox.setValue(50)
        self.lineWidthSpinBox.setValue(0.2)
        self.cornersCheckBox.setChecked(False)
        self.cornersSpinBox.setValue(5)
        self.xSpinBox.setValue(0)
        self.ySpinBox.setValue(0)

    def onCornersCheckBoxChangedState(self, checked):
        self.cornersSpinBox.setEnabled(bool(checked))

    def onSaveButtonClicked(self):
        filename = self.inputFileLineEdit.text()

        if not filename:
            QtGui.QMessageBox.warning(self, 'Error', 'No input file was specified!')
        else:
            reply = QtGui.QMessageBox.question(self, 'Attention', 'File will be overwritten.\nDo you still want to proceed?',
                                               QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

            if reply == QtGui.QMessageBox.Yes:
                # Extract values from interface
                filename = self.inputFileLineEdit.text()
                length = self.lengthSpinBox.value()
                width = self.widthSpinBox.value()
                line_width = self.lineWidthSpinBox.value()
                rounded = self.cornersCheckBox.isChecked()
                if rounded:
                    corners_radius = self.cornersSpinBox.value()
                else:
                    corners_radius = 0
                x = self.xSpinBox.value()
                y = self.ySpinBox.value()

                # Create a KicadBoard
                board = KicadBoard(filename)

                # Add outline
                board.add_rect_outline_at_point((x,y), length, width, corners_radius, line_width)

                # Save result
                board.save()
                QtGui.QMessageBox.information(self, 'Done!', 'Operation performed successfully')


    def onInputFileButtonClicked(self):
        filename, filter = QtGui.QFileDialog.getOpenFileName(parent=self, caption='Open file', dir='.', filter='Kicad PCB Files (*.kicad_pcb)')

        if filename:
            self.inputFileLineEdit.setText(filename)

    def onExportButtonClicked(self):
        in_filename = self.inputFileLineEdit.text()

        if not in_filename:
            QtGui.QMessageBox.warning(self, 'Error', 'No input file was specified!')
        else:
            # Ask for the output filename
            out_filename, filter = QtGui.QFileDialog.getSaveFileName(parent=self, caption='Select output file', dir='.', filter='Kicad PCB Files (*.kicad_pcb)')

            if out_filename:
                if '.kicad_pcb' != out_filename[-10:]:
                    out_filename += '.kicad_pcb'

                # Extract values from interface
                length = self.lengthSpinBox.value()
                width = self.widthSpinBox.value()
                line_width = self.lineWidthSpinBox.value()
                rounded = self.cornersCheckBox.isChecked()
                if rounded:
                    corners_radius = self.cornersSpinBox.value()
                else:
                    corners_radius = 0
                x = self.xSpinBox.value()
                y = self.ySpinBox.value()

                # Create a KicadBoard
                board = KicadBoard(in_filename)

                # Add outline
                board.add_rect_outline_at_point((x,y), length, width, corners_radius, line_width)

                # Save result
                board.save(out_filename)
                QtGui.QMessageBox.information(self, 'Done!', 'Operation performed successfully')



if __name__ == '__main__':

    # Create Qt app
    app = QtGui.QApplication(sys.argv)

    # Create the widget and show it
    gui = PCBOutlineCreator()
    gui.show()

    # Run the app
    sys.exit(app.exec_())