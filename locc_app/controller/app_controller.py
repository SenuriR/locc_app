import sys
from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow
from model.quantum_model import QuantumModel

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.model = QuantumModel()  # Create the model
        self.view = MainWindow(self)  # Pass the controller to the view

    def run(self):
        # Show the main window and start the event loop
        self.view.show()
        sys.exit(self.app.exec_())

    def perform_operation(self, operation_name, *args):
        """
        Handle operations requested by the view, e.g., manipulating quantum states.
        """
        if operation_name == "initialize_quantum_state":
            result = self.model.initialize_quantum_state(*args)
            self.view.display_message(f"Initialized state: {result}")
        elif operation_name == "execute_locc_protocol":
            result = self.model.execute_locc_protocol(*args)
            self.view.display_message(f"LOCC protocol result: {result}")
        else:
            self.view.display_message(f"Unknown operation: {operation_name}")
