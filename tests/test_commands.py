# tests/test_commands.py
import unittest
from commands import *
from canvas import Canvas

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas()
        self.canvas.initialize_canvas(50, 50)

    def tearDown(self):
        # Clear canvas state between tests
        if self.canvas.state is not None:
            self.canvas.state = None
            self.canvas.width = None
            self.canvas.height = None
            self.canvas._initialized = False

    def test_line_command(self):
        cmd = LineCmd(self.canvas)
        
        # Test horizontal line
        cmd.process(["L", "1", "1", "3", "1", "x"])
        self.assertEqual(self.canvas.state[1][1], 'x')
        self.assertEqual(self.canvas.state[1][2], 'x')
        self.assertEqual(self.canvas.state[1][3], 'x')
        
        # Test vertical line
        cmd.process(["L", "1", "1", "1", "3", "x"])
        self.assertEqual(self.canvas.state[1][1], 'x')
        self.assertEqual(self.canvas.state[2][1], 'x')
        self.assertEqual(self.canvas.state[3][1], 'x')
        
        # Test invalid coordinates
        cmd.process(["L", "-1", "1", "3", "1", "x"])
        cmd.process(["L", "1", "-1", "3", "1", "x"])
        cmd.process(["L", "1", "1", "6", "1", "x"])
        cmd.process(["L", "1", "1", "1", "6", "x"])

    def test_diagonal_line_command(self):
        cmd = LineCmd(self.canvas)
        cmd.process(["L", "2", "2", "8", "8", "x"])
        for x in range (2,2) :
            for y in range(8, 8):
                cell = self.canvas.state[y][x]
                self.assertEqual(cell, "x")
        
        #Not Diagonal Line
        cmd.process(["L", "10", "10", "10", "12", "x"])
        self.assertNotEqual(self.canvas.state[11][11], "x")

        cmd.process(["L", "2", "10", "10", "2", "x"])
        self.assertEqual(self.canvas.state[10][2], "x")
        self.assertEqual(self.canvas.state[9][3], "x")
        self.assertEqual(self.canvas.state[8][4], "x")
        self.assertEqual(self.canvas.state[2][10], "x")

    def test_rectangle_command(self):
        cmd = RectangleCmd(self.canvas)
        
        # Test valid rectangle
        cmd.process(["R", "1", "1", "3", "3", "x"])
        # Check corners
        self.assertEqual(self.canvas.state[1][1], 'x')
        self.assertEqual(self.canvas.state[1][3], 'x')
        self.assertEqual(self.canvas.state[3][1], 'x')
        self.assertEqual(self.canvas.state[3][3], 'x')
        # Check sides
        self.assertEqual(self.canvas.state[1][2], 'x')
        self.assertEqual(self.canvas.state[2][1], 'x')
        self.assertEqual(self.canvas.state[2][3], 'x')
        self.assertEqual(self.canvas.state[3][2], 'x')
        
        # Test invalid coordinates
        cmd.process(["R", "-1", "1", "3", "3", "x"])
        cmd.process(["R", "1", "-1", "3", "3", "x"])
        cmd.process(["R", "1", "1", "6", "3", "x"])
        cmd.process(["R", "1", "1", "3", "6", "x"])

    def test_bucket_fill(self):
        cmd = BucketFillCmd(self.canvas)
        
        # Create a rectangle
        rect_cmd = RectangleCmd(self.canvas)
        rect_cmd.process(["R", "1", "1", "3", "3", "x"])
        
        # Fill inside the rectangle
        cmd.process(["B", "2", "2", "o"])
        self.assertEqual(self.canvas.state[2][2], 'o')
        
        # Fill outside the rectangle
        cmd.process(["B", "0", "0", "o"])
        self.assertEqual(self.canvas.state[0][0], 'o')
        
        # Test invalid coordinates
        cmd.process(["B", "-1", "0", "o"])
        cmd.process(["B", "0", "-1", "o"])
        cmd.process(["B", "6", "0", "o"])
        cmd.process(["B", "0", "6", "o"])

    def test_empty_command(self):
        cmd = EmptyCommand(self.canvas)
        
        # Fill canvas with some content
        line_cmd = LineCmd(self.canvas)
        line_cmd.process(["L", "1", "1", "3", "1", "x"])
        
        # Clear canvas
        cmd.process(["E"])
        
        # Verify canvas is empty
        for row in self.canvas.state:
            for cell in row:
                self.assertEqual(cell, ' ')


    def test_undo_command(self):
        cmd = UndoCommand(self.canvas)

        #Fill Canvas
        line_cmd = LineCmd(self.canvas)
        line_cmd.process(["L", "1", "1", "3", "1", "x"])

        cmd.process(["U"])
        for x in range (1,4) :
            for y in range(1, 2):
                cell = self.canvas.state[y][x]
                self.assertEqual(cell, ' ')