from PySide import QtCore,QtGui
from PySide import QtUiTools
import os, sys

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
        # Call the constructor to create the C++ object instance and avoid errors (that happen sometimes)
        QtGui.QWidget.__init__(self, parent)

        # Load the UI on this class
        ui_file_path = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'PCBOutlineCreator.ui')
        load_ui(ui_file_path, self)
        self.main_widget = self.findChild(QtGui.QWidget)

        # Connect callbacks
        self.main_widget.inputFileButton.clicked.connect(self.onInputFileButtonClicked)

        # Configure control ranges:
        max_float = sys.float_info.max
        self.main_widget.lengthSpinBox.setMinimum(0)
        self.main_widget.lengthSpinBox.setMaximum(max_float)
        self.main_widget.widthSpinBox.setMinimum(0)
        self.main_widget.widthSpinBox.setMaximum(max_float)
        self.main_widget.lineWidthSpinBox.setMinimum(0)
        self.main_widget.lineWidthSpinBox.setMaximum(max_float)
        self.main_widget.lineWidthSpinBox.setSingleStep(0.1)
        self.main_widget.cornersSpinBox.setMinimum(0)
        self.main_widget.cornersSpinBox.setMaximum(max_float)
        self.main_widget.xSpinBox.setMinimum(0)
        self.main_widget.xSpinBox.setMaximum(max_float)
        self.main_widget.ySpinBox.setMinimum(0)
        self.main_widget.ySpinBox.setMaximum(max_float)

        # Default values
        self.default()

    def default(self):
        self.main_widget.lengthSpinBox.setValue(50)
        self.main_widget.widthSpinBox.setValue(50)
        self.main_widget.lineWidthSpinBox.setValue(0.2)
        self.main_widget.cornersSpinBox.setEnabled(False)

    def onInputFileButtonClicked(self):
        pass



if __name__ == '__main__':

    # Create Qt app
    app = QtGui.QApplication(sys.argv)

    # Create the widget and show it
    gui = PCBOutlineCreator()
    gui.show()

    # Run the app
    sys.exit(app.exec_())