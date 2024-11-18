from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, 
    QVBoxLayout, QWidget, QMessageBox, QLabel, QLineEdit, QSizePolicy, QHBoxLayout, QComboBox, QScrollArea, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        # Set up the main window
        self.setWindowTitle("Quantum State Input and Operations")
        # self.setGeometry(100, 100, 600, 600)
        self.setGeometry(100, 60, 500, 800)
        self.setFixedSize(self.width(), self.height())
        self.fixed_width = 50

        # Create a scroll area and set it as the central widget
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setCentralWidget(scroll_area)

        # Create a widget for the scroll area and set its layout
        scroll_widget = QWidget()
        scroll_area.setWidget(scroll_widget)
        self.layout = QVBoxLayout(scroll_widget)

        self.layout.setContentsMargins(10,10,10,10)

        # Alternatively, you can add a QSpacerItem to the layout
        spacer = QSpacerItem(20, 0, QSizePolicy.Fixed, QSizePolicy.Minimum)
        self.layout.addItem(spacer)

        table_h_layout = QHBoxLayout()

        # Create a table widget for amplitude and basis state input
        self.table = QTableWidget(0, 2)  # Initially zero rows, 2 columns
        self.table.setHorizontalHeaderLabels(["Amplitude", "Basis State"])

        self.table.setFixedSize(300,200)
        table_h_layout.addWidget(self.table, alignment=Qt.AlignLeft)

        add_remove_v_layout = QVBoxLayout()
        add_remove_v_layout.setSpacing(5)  # Set spacing to 5 pixels (or any small value)
        add_remove_v_layout.setContentsMargins(0,0,0,0)

        # Add buttons to add/remove rows
        self.add_row_button = QPushButton("Add Row")
        self.add_row_button.clicked.connect(self.add_row)
        self.add_row_button.setFixedSize(100,30)
        add_remove_v_layout.addWidget(self.add_row_button, alignment=Qt.AlignCenter)

        self.remove_row_button = QPushButton("Remove Row")
        self.remove_row_button.clicked.connect(self.remove_row)
        self.remove_row_button.setFixedSize(100,30)
        add_remove_v_layout.addWidget(self.remove_row_button, alignment=Qt.AlignCenter)
        
        table_h_layout.addLayout(add_remove_v_layout)
        self.layout.addLayout(table_h_layout)

        # Function Buttons Layout
        self.function_buttons_layout = QHBoxLayout()
        self.layout.addLayout(self.function_buttons_layout)

        # Dictionary of allowed functions with formatted strings
        self.allowed_functions = {
            'SQRT': 'np.sqrt()',
            'PI': 'np.pi',
            'SIN': 'np.sin()',
            'COS': 'np.cos()',
            'EXP': 'np.exp()',
        }

        # Add function buttons
        for func_name, func_str in self.allowed_functions.items():
            button = QPushButton(func_name)
            button.clicked.connect(lambda _, f=func_str: self.insert_function(f))
            self.function_buttons_layout.addWidget(button)

        # Add a button to create the quantum state
        self.create_state_button = QPushButton("Create Quantum State")
        self.create_state_button.clicked.connect(self.handle_create_state)
        self.create_state_button.setFixedSize(200,30)
        self.layout.addWidget(self.create_state_button, alignment=Qt.AlignCenter)

        party_h_layout = QHBoxLayout()
        party_h_layout.setSpacing(0)
        party_h_layout.setContentsMargins(0, 0, 275, 0)


        self.num_parties_label = QLabel("Number of parties (k):")
        self.num_parties_input = QLineEdit()
        self.num_parties_input.setFixedWidth(self.fixed_width)
        party_h_layout.addWidget(self.num_parties_label)
        party_h_layout.addWidget(self.num_parties_input)
        self.layout.addLayout(party_h_layout)
        
        # input for number of qudits per party
        qudits_h_layout = QHBoxLayout()
        qudits_h_layout.setSpacing(0)
        qudits_h_layout.setContentsMargins(0, 0, 100, 0)

        self.num_qudits_label = QLabel("Number of qudits for each party (comma-separated):")
        self.num_qudits_input = QLineEdit()
        self.num_qudits_input.setFixedWidth(self.fixed_width)
        qudits_h_layout.addWidget(self.num_qudits_label)
        qudits_h_layout.addWidget(self.num_qudits_input)
        self.layout.addLayout(qudits_h_layout)

        # Input for dimension
        dim_h_layout = QHBoxLayout()
        dim_h_layout.setSpacing(0)
        dim_h_layout.setContentsMargins(0, 0, 300, 0)

        self.dim_label = QLabel("Dimension of qudits:")
        self.dim_input = QLineEdit()
        self.dim_input.setFixedWidth(self.fixed_width)
        dim_h_layout.addWidget(self.dim_label)
        dim_h_layout.addWidget(self.dim_input)
        self.layout.addLayout(dim_h_layout)

        # Button to generate state description label
        self.generate_button = QPushButton("Generate State Descriptor and K Party")
        self.generate_button.clicked.connect(self.handle_generate_state_desc_label_and_k_party)
        self.generate_button.setFixedSize(300,30)
        self.layout.addWidget(self.generate_button, alignment=Qt.AlignCenter)

        self.header_widget = QWidget()
        self.header_layout = QVBoxLayout(self.header_widget)

        self.header_layout.addWidget(QLabel("LOCC Operation Creator"), alignment=Qt.AlignCenter)
        h_layout1 = QHBoxLayout()
        self.locc_entry = QLineEdit()
        h_layout1.addWidget(QLabel("Number of Steps in Procotol:"))
        h_layout1.addWidget(self.locc_entry)

        add_locc_button = QPushButton("Add LOCC Entries")
        add_locc_button.clicked.connect(self.handle_add_locc_ui)
        h_layout1.addWidget(add_locc_button)

        self.header_layout.addLayout(h_layout1)
        self.layout.addWidget(self.header_widget)
        self.locc_frame = QWidget()
        self.locc_frame.setFixedWidth(self.width() - 20)
        self.locc_frame_layout = QVBoxLayout(self.locc_frame)
        self.locc_frame_layout.setSpacing(1)
        self.locc_frame_layout.setContentsMargins(10,10,10,10)
        self.layout.addWidget(self.locc_frame)

    def handle_add_locc_ui(self):

        # Clear previous entries
        while self.locc_frame_layout.count():
            item = self.locc_frame_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            elif item.layout() is not None:
                self.clear_layout(item.layout())
            del item

        # Validate input
        if self.locc_entry_text == '':
            QMessageBox.critical(
                self.parent_gui, "Input Error",
                "Enter an integer value in 'Number of steps in LOCC protocol (number of locc objects)' field."
            )
            return None

        try:
            num_steps = int(self.locc_entry_text)
        except ValueError:
            QMessageBox.critical(
                self.parent_gui, "Input Error",
                "Invalid input. Enter a valid integer."
            )
            return None

        self.locc_step_widgets.clear()

        # Conditional operation entries
        cond_text = QLabel("Leave the condition entry empty if the step is NOT a CONDITIONAL OPERATION.")
        cond_text.setAlignment(Qt.AlignCenter)

        # Dynamically add LOCC entries
        for i in range(num_steps):
            self.curr_step_widgets = {}
            # Operation type selection
            h_layout = QHBoxLayout()
            h_layout.setContentsMargins(0, 10, 150, 0)
            h_layout.setSpacing(0)
            operation_type_combobox = QComboBox()
            operation_type_combobox.addItems(["select operation type...", "measurement", "conditional"])
            h_layout.addWidget(QLabel("Operation Type:"))
            h_layout.addWidget(operation_type_combobox)
            self.locc_frame_layout.addLayout(h_layout)
            self.curr_step_widgets['operation_type_combobox'] = operation_type_combobox

            # Operator, party index, and qudit index
            operator_party_qudit_layout = QHBoxLayout()
            operator_party_qudit_layout.setContentsMargins(0,10,10,0)
            operator_party_qudit_layout.addWidget(QLabel("Operator"))
            operator_combobox = QComboBox()
            operator_combobox.addItems(["XGate", "HGate", "CXGate"])
            operator_party_qudit_layout.addWidget(operator_combobox)
            self.curr_step_widgets['operator_combobox'] = operator_combobox

            party_index_entry = QLineEdit()
            party_index_entry.setFixedWidth(self.fixed_width)
            operator_party_qudit_layout.addWidget(QLabel("Party Index:"))
            operator_party_qudit_layout.addWidget(party_index_entry)
            self.curr_step_widgets['party_index_entry'] = party_index_entry

            qudit_index_entry = QLineEdit()
            qudit_index_entry.setFixedWidth(self.fixed_width)
            operator_party_qudit_layout.addWidget(QLabel("Qudit Index:"))
            operator_party_qudit_layout.addWidget(qudit_index_entry)
            self.curr_step_widgets['qudit_index_entry'] = qudit_index_entry

            self.locc_frame_layout.addLayout(operator_party_qudit_layout)

            cond_h_layout = QHBoxLayout()
            cond_h_layout.setSpacing(0)
            cond_h_layout.setContentsMargins(0, 10, 125, 0)
            cond_info_entry = QLineEdit()
            cond_info_entry.setFixedWidth(self.fixed_width)
            cond_h_layout.addWidget(QLabel("Condition Entry Info (party, qudit, result):"))
            cond_h_layout.addWidget(cond_info_entry)

            self.locc_frame_layout.addLayout(cond_h_layout)

            # Save button for each step
            save_locc_entry_button = QPushButton("Save LOCC step entry")
            save_locc_entry_button.clciked.connect(self.handle_save_locc_entry)
            self.locc_frame_layout.addWidget(save_locc_entry_button)

            # Spacer after each step
            spacer_2 = QSpacerItem(40, 40, QSizePolicy.Minimum, QSizePolicy.Minimum)
            self.locc_frame_layout.addSpacerItem(spacer_2)

            # Add step widgets to the list
            self.locc_step_widgets.append(self.curr_step_widgets)

        create_locc_protocol_button = QPushButton("Create LOCC Protocol")
        create_locc_protocol_button.clicked.connect(self.handle_create_locc_protocol)
        self.locc_frame_layout.addWidget(create_locc_protocol_button)

    def handle_create_locc_protocol(self):
        self.controller.perform_operation("create_locc_protocol")
    
    def handle_save_locc_entry(self):
        try:
            # Extract basic values from widgets
            party_index = int(self.curr_step_widgets['party_index_entry'].text())
            qudit_index = int(self.curr_step_widgets['qudit_index_entry'].text())
            operation_type = self.curr_step_widgets['operation_type_combobox'].currentText()
            operator_choice = self.curr_step_widgets['operator_combobox'].currentText()
            condition = None
            if operation_type == "conditional":
                cond_info_list = list(map(int, self.cond_info_entry.text().split(',')))
                condition = (cond_info_list[0], cond_info_list[1], cond_info_list[2]) # party, qudit, result
            
            self.controller.perform_operation("save_locc_step", party_index, qudit_index, operation_type, operator_choice, condition)

        except ValueError:
            # Show error message when inputs are invalid
            QMessageBox.critical(self.parent_gui, "Input Error", "Enter valid integer values.")

    def add_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
    
    def remove_row(self):
        current_row = self.table.currentRow()
        if current_row >= 0:
            self.table.removeRow(current_row)

    def handle_generate_state_desc_label_and_k_party(self):
        self.controller.perform_operation("generate_state_desc_label_and_k_party", self.num_parties_input, self.num_qudits_input, self.dim_input)

    def handle_create_state(self):
        amplitude_list, basis_state_list = self.get_table_data()
        self.controller.perform_operation("create_quantum_state", amplitude_list, basis_state_list)

    def display_message(self, message):
        # Display a message to the user
        QMessageBox.information(self, "Information", message)

    def get_table_data(self):
        # Allowed functions for user input
        allowed_functions = {
            'np': np,
            'sqrt': np.sqrt,
            'pi': np.pi,
            'sin': np.sin,
            'cos': np.cos,
            'exp': np.exp,
            'j': 1j,
            'I': 1j,
        }

        amplitude_list = []
        basis_state_list = []

        for row in range(self.table.rowCount()):
            amplitude_item = self.table.item(row, 0)
            if amplitude_item is None or not amplitude_item.text():
                raise ValueError(f"Missing amplitude in row {row}.")
            amplitude_str = amplitude_item.text()

            # Safely evaluate the amplitude string using allowed functions
            amplitude = eval(amplitude_str, {"__builtins__": {}}, allowed_functions)

            state_item = self.table.item(row, 1)
            if state_item is None or not state_item.text():
                raise ValueError(f"Missing basis state in row {row}.")
            basis_state = state_item.text()

            if not basis_state.isdigit():
                raise ValueError(f"Invalid basis state '{basis_state}' in row {row}. Must be digits only.")

            amplitude_list.append(amplitude)
            basis_state_list.append(basis_state)
            return amplitude_list, basis_state_list
        
    def handle_execute_protocol(self):
        # Call the controller to handle the action
        self.controller.perform_operation("execute_locc_protocol", {"protocol": "example"})