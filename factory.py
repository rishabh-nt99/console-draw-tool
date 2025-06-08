from commands import *

class CommandFactory:
    def __init__(self, canvas):
      self.canvas=canvas

    _command_map= {
      "C": CreateCanvasCmd,
      "L": LineCmd,
      "R": RectangleCmd,
      "B": BucketFillCmd,
      "Q": QuitCmd,
      "E": EmptyCommand,
    }
    def get_command(self, input):
        try:
            if input is None:
                print("Error: Input cannot be None")
                return None
            if not isinstance(input, list):
                print(f"Error: Expected list input, got {type(input).__name__}")
                return None
            if len(input) == 0:
                print("Error: Empty command input")
                return None
            try:
                command_key = str(input[0]).upper()
            except (AttributeError, TypeError):
                print(f"Error: Invalid command key type: {type(input[0]).__name__}")
                return None
                
            command_class = CommandFactory._command_map.get(command_key)
            if not command_class:
                print(f"Invalid Command: {command_key}")
                return None
            
            return command_class(self.canvas)
            
        except Exception as e:
            print(f"Unexpected error in get_command: {str(e)}")
            return None
    
    def print_help_text(self) -> str:
        print("\n================== Console Drawing Tool Commands ==================\n")
        for cmd_key, cmd_class in self._command_map.items():
            cmd = cmd_class(self.canvas)
            print(f"{cmd_key})  {cmd.get_help_text()}")
        print("\nNote: All coordinates are zero-based (start from 0)")
        print("The canvas is displayed with (0,0) at the bottom-left")
        print("\n================== *-*-*-*-*-*-*-*-*-*-*-*-*-*-* ==================\n")