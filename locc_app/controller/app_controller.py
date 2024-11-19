import sys
from PyQt5.QtWidgets import QApplication
from view.main_window import MainWindow
from model.quantum_model import QuantumModel
from model.video_model import VideoModel
import subprocess
import os
import platform

class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.model = QuantumModel()  # Create the model
        self.video_model = VideoModel() # New video model
        self.view = MainWindow(self)  # Pass the controller to the view

    def run(self):
        # Show the main window and start the event loop
        self.view.show()
        sys.exit(self.app.exec_())

    def generate_manim_video(self, text: str):
        """
        Generate a Manim video by delegating to the model and updating the view.
        """
        self.model.check_before_video() # to ensure locc procotol and k party objs are created with our quantum model

        try:
            video_path = self.video_model.generate_video(text)
            self.view.display_message("Video generated successfully!")
            self.play_video_with_os_player(video_path)
        except Exception as e:
            self.view.display_message(f"Error generating video: {str(e)}")
    
    def play_video_with_os_player(self, video_path):
        """
        Play the generated video using the user's operating system video player.
        """
        try:
            if platform.system() == "Windows":
                os.startfile(video_path)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", video_path])
            else:  # Linux and other Unix-like systems
                subprocess.run(["xdg-open", video_path])
        except Exception as e:
            self.view.display_message(f"Could not play video: {str(e)}")


    def perform_operation(self, operation_name, *args):
        """
        Handle operations requested by the view, e.g., manipulating quantum states.
        """
        if operation_name == "create_quantum_state":
            result = self.model.create_quantum_state(*args) 
            self.view.display_message(f"Initialized state: {result}")
        elif operation_name == "generate_state_desc_label_and_k_party":
            result = self.model.generate_state_desc_label_and_k_party(*args)
            self.view.display_message(f"{result}")
        elif operation_name == "save_locc_operation":
            result = self.model.save_locc_operation(*args)
            self.view.display_message(f"{result}")
        else:
            self.view.display_message(f"Unknown operation: {operation_name}")
