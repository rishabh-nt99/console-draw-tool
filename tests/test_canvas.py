# tests/test_canvas.py
import unittest
from canvas import Canvas

class TestCanvas(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas()

    def tearDown(self):
        # Clear canvas state between tests
        if self.canvas.state is not None:
            self.canvas.state = None
            self.canvas.width = None
            self.canvas.height = None
            self.canvas._initialized = False

    def test_initialize_canvas(self):
        # Test valid initialization
        self.canvas.initialize_canvas(5, 5)
        self.assertEqual(self.canvas.width, 5)
        self.assertEqual(self.canvas.height, 5)
        self.assertEqual(len(self.canvas.state), 5)
        self.assertEqual(len(self.canvas.state[0]), 5)

    def test_invalid_initialize_canvas(self):
        # Test invalid dimensions
        self.canvas.initialize_canvas(-1, 5)
        self.assertIsNone(self.canvas.state)
        self.canvas.initialize_canvas(5, -1)
        self.assertIsNone(self.canvas.state)
        self.canvas.initialize_canvas(0, 5)
        self.assertIsNone(self.canvas.state)
        self.canvas.initialize_canvas(5, 0)
        self.assertIsNone(self.canvas.state)
    
    def test_validate_coordinates(self):
        self.canvas.initialize_canvas(5, 5)
        
        # Test valid coordinates
        self.assertTrue(self.canvas.validate_coordinates(0, 0))
        self.assertTrue(self.canvas.validate_coordinates(4, 4))
        self.assertTrue(self.canvas.validate_coordinates(2, 2))
        
        # Test invalid coordinates
        self.assertFalse(self.canvas.validate_coordinates(-1, 0))
        self.assertFalse(self.canvas.validate_coordinates(0, -1))
        self.assertFalse(self.canvas.validate_coordinates(5, 0))
        self.assertFalse(self.canvas.validate_coordinates(0, 5))
        
        # Test two points validation
        self.assertTrue(self.canvas.validate_coordinates(0, 0, 4, 4))
        self.assertFalse(self.canvas.validate_coordinates(0, 0, 5, 5))
        self.assertFalse(self.canvas.validate_coordinates(-1, 0, 4, 4))

    def test_singleton(self):
        canvas1 = Canvas()
        canvas2 = Canvas()
        self.assertIs(canvas1, canvas2)
        
        # Test that state is shared
        canvas1.initialize_canvas(5, 5)
        self.assertEqual(canvas2.width, 5)
        self.assertEqual(canvas2.height, 5)

    def test_print_canvas(self):
        self.canvas.initialize_canvas(3, 3)
        # Test that print_canvas doesn't raise any exceptions
        try:
            self.canvas.print_canvas()
        except Exception as e:
            self.fail(f"print_canvas raised {type(e).__name__} unexpectedly!")

    def test_canvas_state_after_initialization(self):
        self.canvas.initialize_canvas(3, 3)
        # Check that all cells are empty spaces
        for row in self.canvas.state:
            for cell in row:
                self.assertEqual(cell, ' ')