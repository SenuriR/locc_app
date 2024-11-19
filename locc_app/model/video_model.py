from manim import config, Scene, Text, Write

class VideoModel:
    def __init__(self):
        self.video_path = None  # Store the path of the generated video

    def generate_video(self, text: str, output_path: str = "manim_output.mp4"):
        """
        Generate a Manim video with the given text and save it to the specified path.
        """
        # Update Manim's configuration for the output file
        config.media_dir = "./media"
        config.output_file = output_path

        class VideoScene(Scene):
            def construct(self):
                title = Text(text)
                self.play(Write(title))
                self.wait(2)

        # Generate the video
        VideoScene().render()
        self.video_path = config.output_file
        return self.video_path
