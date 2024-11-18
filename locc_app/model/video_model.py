from manim import Scene, Text, Write

class VideoModel:
    def __init__(self):
        self.video_path = None  # Store the path of the generated video

    def generate_video(self, text: str, output_path: str = "manim_output.mp4"):
        """
        Generate a Manim video with the given text and save it to the specified path.
        """
        class VideoScene(Scene):
            def construct(self):
                title = Text(text)
                self.play(Write(title))
                self.wait(2)

        # Generate the video
        VideoScene().render(output_file_path=output_path)
        self.video_path = output_path
        return self.video_path
