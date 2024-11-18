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
        if operation_name == "create_quantum_state":
            result = self.model.create_quantum_state(*args) 
            self.view.display_message(f"Initialized state: {result}")
        elif operation_name == "generate_state_desc_label_and_k_party":
            result = self.model.generate_state_desc_label(*args)
            self.view.display_message(f"{result}")
        elif operation_name == "save_locc_step":
            result = self.model.add_locc_step(*args)
            self.view.display_message(f"{result}")
        elif operation_name == "create_locc_protocol":
            result = self.model.create_locc_protocol
            self.view.display_message(f"{result}")
        else:
            self.view.display_message(f"Unknown operation: {operation_name}")
