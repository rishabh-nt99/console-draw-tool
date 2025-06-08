import unittest
from commands import (
    CreateCanvasCmd, LineCmd, RectangleCmd, 
    BucketFillCmd, QuitCmd, EmptyCommand
)
from canvas import Canvas

class TestCanvasCreateCommands(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas()

    def tearDown(self):
        # Clear canvas state between tests
        if self.canvas.state is not None:
            self.canvas.state = None
            self.canvas.width = None
            self.canvas.height = None
            self.canvas._initialized = False

    def test_create_canvas(self):
        cmd = CreateCanvasCmd(self.canvas)
        
        # Test valid creation
        cmd.process(["C", "3", "3"])
        self.assertEqual(self.canvas.width, 3)
        self.assertEqual(self.canvas.height, 3)
        
    def test_invalid_create_canvas(self):
        cmd = CreateCanvasCmd(self.canvas)

        # Test invalid inputs
        cmd.process(["C", "a", "3"])  # Non-integer width
        cmd.process(["C", "3", "b"])  # Non-integer height
        cmd.process(["C", "-1", "3"])  # Negative width
        cmd.process(["C", "3", "-1"])  # Negative height
        cmd.process(["C", "0", "3"])   # Zero width
        cmd.process(["C", "3", "0"])   # Zero height