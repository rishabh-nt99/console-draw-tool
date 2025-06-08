# tests/test_factory.py
import unittest
from factory import CommandFactory
from commands import (
    CreateCanvasCmd, LineCmd, RectangleCmd, 
    BucketFillCmd, QuitCmd, EmptyCommand
)
from canvas import Canvas

class TestFactory(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas()
        self.factory = CommandFactory(self.canvas)

    def test_get_command(self):
        # Test valid commands
        self.assertIsInstance(self.factory.get_command(["C"]), CreateCanvasCmd)
        self.assertIsInstance(self.factory.get_command(["L"]), LineCmd)
        self.assertIsInstance(self.factory.get_command(["R"]), RectangleCmd)
        self.assertIsInstance(self.factory.get_command(["B"]), BucketFillCmd)
        self.assertIsInstance(self.factory.get_command(["Q"]), QuitCmd)
        self.assertIsInstance(self.factory.get_command(["E"]), EmptyCommand)
        
        # Test invalid command
        self.assertIsNone(self.factory.get_command(["X"]))
        
        # Test case insensitivity
        self.assertIsInstance(self.factory.get_command(["c"]), CreateCanvasCmd)
        self.assertIsInstance(self.factory.get_command(["l"]), LineCmd)
        self.assertIsInstance(self.factory.get_command(["r"]), RectangleCmd)
        self.assertIsInstance(self.factory.get_command(["b"]), BucketFillCmd)
        self.assertIsInstance(self.factory.get_command(["q"]), QuitCmd)
        self.assertIsInstance(self.factory.get_command(["e"]), EmptyCommand)

    def test_get_command_with_empty_input(self):
        # Test empty input
        self.assertIsNone(self.factory.get_command([]))
        
        # Test None input
        self.assertIsNone(self.factory.get_command(None))

    def test_get_command_with_invalid_input(self):
        # Test non-string input
        self.assertIsNone(self.factory.get_command(['1']))
        
        # Test empty string
        self.assertIsNone(self.factory.get_command([""]))

    # def test_help_text(self):
    #     help_text = self.factory.get_help_text()
    #     self.assertIsNotNone(help_text)
    #     self.assertIn("Console Drawing Tool Commands", help_text)
    #     self.assertIn("Create a new canvas", help_text)
    #     self.assertIn("Draw a line", help_text)
    #     self.assertIn("Draw a rectangle", help_text)
    #     self.assertIn("Fill the area", help_text)
        
    #     # Test that all commands are listed
    #     for cmd_key in self.factory._command_map.keys():
    #         self.assertIn(f"{cmd_key})", help_text)