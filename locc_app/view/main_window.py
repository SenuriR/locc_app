from PyQt5.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QMessageBox

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        # Set up the main window UI
        self.setWindowTitle("LOCC App")
        self.setGeometry(100, 100, 600, 400)

        # Example buttons for user actions
        self.initialize_button = QPushButton("Initialize Quantum State")
        self.execute_button = QPushButton("Execute LOCC Protocol")

        # Connect buttons to actions
        self.initialize_button.clicked.connect(self.handle_initialize_state)
        self.execute_button.clicked.connect(self.handle_execute_protocol)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.initialize_button)
        layout.addWidget(self.execute_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def handle_initialize_state(self):
        # Call the controller to handle the action
        self.controller.perform_operation("initialize_quantum_state", [0, 1, 0])  # Example args

    def handle_execute_protocol(self):
        # Call the controller to handle the action
        self.controller.perform_operation("execute_locc_protocol", {"protocol": "example"})

    def display_message(self, message):
        # Display a message to the user
        QMessageBox.information(self, "Information", message)
