from abc import ABC, abstractmethod
from canvas import Canvas
import sys

from history_stack import HistoryStack


class Command(ABC):
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.history_stack = HistoryStack()

    @abstractmethod
    def execute(self, input: list[str]):
        pass
    
    @abstractmethod
    def validate(self, input: list[str]) -> bool:
        pass
    
    @abstractmethod
    def get_help_text(self) -> str:
        """Return the help text for this command"""
        pass
    
    def process(self, input):
        if(self.validate(input)):
            self.execute(input)
            self.canvas.print_canvas()



class CreateCanvasCmd(Command):

    def execute(self, input):
        self.canvas.initialize_canvas(int(input[1]), int(input[2]))
    
    def validate(self, input: list[str]):
        if len(input) < 3:
            print("Too little input. Expected format: C width<int> height<int>")
            return False
        elif not input[1].isdigit() or not input[2].isdigit():
            print("Width and Height must be integers. Expected format: C width<int> height<int>")
            return False
        elif int(input[1]) <= 0 or int(input[2]) <= 0: 
            print("Width and Height must be positive integers. Expected format: C width<int> height<int>")
            return False
        elif len(input) > 3:
            print('Too many arguments. Ignoring extra arguments.')
        return True
    
    def get_help_text(self) -> str:
        return (
            "width<int> height<int>                   |  Create a new canvas of width w and height h\n"
            "                                             |  Example: C 20 4\n"
            "                                             | "
        )
    

class LineCmd(Command):
    def execute(self, input: list[str]):
        x1, y1 = int(input[1]), int(input[2])
        x2, y2 = int(input[3]), int(input[4])
        char = input[5]
        current_changes = []
        dx, dy = x2-x1, y2-y1

        # M<1 = negative diagonal
        # M>1 = positive diagonal
        # M=0 horizontal Line
        # M=inf then vertical line
        if dx!=0:
            m = dy//dx
        else:
            m=10000

        if m==10000:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                old_char = self.canvas.state[y][x1]
                self.canvas.state[y][x1] = char
                current_changes.append((x1, y, old_char, char))
        elif m==1 or m==-1: 
            x=x1
            y=y1
            
            sx= 1 if x2>x1 else -1
            sy=1  if y2>y1 else -1
            
            for i in range (abs(dx+1)):
                old_char = self.canvas.state[y][x]
                self.canvas.state[y][x]=char
                current_changes.append((x, y, old_char, char))
                y+=sy
                x+=sx
        elif m==0:
             for x in range(min(x1, x2), max(x1, x2) + 1):
                old_char = self.canvas.state[y1][x]
                self.canvas.state[y1][x] = char
                current_changes.append((x, y1, old_char, char))
        else:
            print("Not a straight line")
 
        # elif m==0:
        #     old_char = self.canvas.state[y1][x]
        #     self.canvas.state[y1][x] = char
        #     current_changes.append((x, y1, old_char, char))
        
        # elif m<0:
        #     x= max(x1,x2)   
        #     for y in range(min(y1,y2), max(y1,y2)+1):
        #         self.canvas.state[y][x]=char
        #         x-=1

        # else
        # if abs(dx)==abs(dy): #We can draw a perfect diagonal
        #     m = dy/dx
        #     if m>0:
        #         for x in range(min(x1,x2), max(x1,x2)+1):
        #             self.canvas.state[x][x]=char 
            
        #     else:
        #        x= max(x1,x2)   
        #        for y in range(min(y1,y2), max(y1,y2)+1):
        #             self.canvas.state[y][x]=char
        #             x-=1
        # elif x1 == x2:  # Vertical line
        #     for y in range(min(y1, y2), max(y1, y2) + 1):
        #         old_char = self.canvas.state[y][x1]
        #         self.canvas.state[y][x1] = char
        #         current_changes.append((x1, y, old_char, char))
        # elif y1 == y2:  # Horizontal line
        #     for x in range(min(x1, x2), max(x1, x2) + 1):
        #         old_char = self.canvas.state[y1][x]
        #         self.canvas.state[y1][x] = char
        #         current_changes.append((x, y1, old_char, char))
        # else:  # L-shaped line (horizontal then vertical)
        #     for x in range(min(x1, x2), max(x1, x2) + 1):
        #         old_char = self.canvas.state[y1][x]
        #         self.canvas.state[y1][x] = char
        #         current_changes.append((x, y1, old_char, char))
        #     y_start = min(y1, y2) if y2 < y1 else y1 + 1
        #     y_end = max(y1, y2) + 1
        #     for y in range(y_start, y_end):
        #         old_char = self.canvas.state[y][x2]
        #         self.canvas.state[y][x2] = char
        #         current_changes.append((x2, y, old_char, char))
        
        self.history_stack.add_to_undo(current_changes)
    
    def validate(self, input: list[str]) -> bool:
        if not self.canvas._initialized:
            print("Canvas not initialized. Please create a canvas first.")
            return False
        
        if len(input) < 6:
            print("Too little input. Expected format: L x1<int> y1<int> x2<int> y2<int> [character]")
            return False
        if len(input) > 6:
            print("Too many arguments.Ignoring Extra characters")
        try:
            x1, y1 = int(input[1]), int(input[2])
            x2, y2 = int(input[3]), int(input[4])
        except ValueError:
            print("All coordinates must be integers. Expected format: L x1<int> y1<int> x2<int> y2<int> [character]")
            return False

        if not self.canvas.validate_coordinates(x1, y1, x2, y2):
            print("Coordinates are not inside the canvas bounds.")
            return False
        
        if len(input[5]) != 1:
            print("Character must be a single character.")
            return False

        return True
    
    def get_help_text(self) -> str:
        return (
            "x1<int> y1<int> x2<int> y2<int> c<char>  |  Draw a line from (x1,y1) to (x2,y2) with character c\n"
            "                                             |  Only horizontal or vertical lines are supported\n"
            "                                             |  Example: L 1 2 6 2 x\n"
            "                                             | "
        )

class RectangleCmd(Command):
    def execute(self, input: list[str]):
        x1, y1 = int(input[1]), int(input[2])
        x2, y2 = int(input[3]), int(input[4])
        char = input[5]
        
        # Top horizontal line
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.canvas.state[y1][x] = char
            
        # Bottom horizontal line
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.canvas.state[y2][x] = char
            
        # Left vertical line
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.canvas.state[y][x1] = char
            
        # Right vertical line
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.canvas.state[y][x2] = char
    
    def validate(self, input: list[str]) -> bool:
        if not self.canvas._initialized:
            print("Canvas not initialized. Please create a canvas first.")
            return False

        if len(input) < 6:
            print("Too little input. Expected format: R x1<int> y1<int> x2<int> y2<int> [character]")
            return False
        if len(input) > 6:
            print("Too many arguments.Ignoring Extra characters")

        try:
            x1, y1 = int(input[1]), int(input[2])
            x2, y2 = int(input[3]), int(input[4])
        except ValueError:
            print("All coordinates must be integers. Expected format: L x1<int> y1<int> x2<int> y2<int> [character]")
            return False

        if not self.canvas.validate_coordinates(x1, y1, x2, y2):
            print("Coordinates are not inside the canvas bounds.")
            return False
        
        if x1 == x2 or y1 == y2:
            print("Coordinates don't form a Rectangle!")
            return False
        
        if len(input[5]) != 1:
            print("Character must be a single character.")
            return False

        return True
    
    def get_help_text(self) -> str:
        return (
            "x1<int> y1<int> x2<int> y2<int> c<char>  |   Draw a rectangle with corners (x1,y1) and (x2,y2) with character c\n"
            "                                             |  Example: R 14 1 18 3 o\n"
            "                                             |  "
        )

class BucketFillCmd(Command):
    def execute(self, input: list[str]):
        x, y = int(input[1]), int(input[2])
        char = input[3]
        target_color = self.canvas.state[y][x]
        if target_color == char:
            return
        
        #Using BFS to find the bucket fill area.
        queue = [(x, y)]
        visited = set()
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
        while queue:
            current_x, current_y = queue.pop(0)
    
            if (current_x, current_y) in visited:
                continue
            if (current_x < 0 or current_x >= self.canvas.width or 
                current_y < 0 or current_y >= self.canvas.height):
                continue
            if self.canvas.state[current_y][current_x] != target_color:
                continue
            visited.add((current_x, current_y))
            self.canvas.state[current_y][current_x] = char
            for dx, dy in directions:
                queue.append((current_x + dx, current_y + dy))
    
    def validate(self, input: list[str]) -> bool:
        if not self.canvas._initialized:
            print("Canvas not initialized. Please create a canvas first.")
            return False
        if len(input) < 4:
            print("Too little input. Expected format: B x<int> y<int> [character]")
            return False
        if len(input) > 4:
            print("Too many arguments. Ignoring extra characters")
        try:
            x, y = int(input[1]), int(input[2])
        except ValueError:
            print("Coordinates must be integers. Expected format: B x<int> y<int> [character]")
            return False
        if not self.canvas.validate_coordinates(x, y):
            print("Coordinates are not inside the canvas bounds.")
            return False
        if len(input[3]) != 1:
            print("Character must be a single character.")
            return False

        return True
    
    def get_help_text(self) -> str:
        return (
            "x<int> y<int> c<char>                    |  Fill the area connected to point (x,y) with character c\n"
            "                                             |  Example: B 10 3 o\n"
            "                                             | "
        )

class QuitCmd(Command):
    def execute(self, input: list[str]):
        print("Thanks for using the draw tool!")
        sys.exit()
    
    def validate(self, input: list[str]) -> bool:
        return True
    
    def get_help_text(self) -> str:
        return(
            "                                         |  Quit the program\n"
            "                                             | "
        )

# Additional Commands Implemented for ease of use
class EmptyCommand(Command):
    def execute(self, input: list[str]):
        print("Canvas Cleared.")
        self.canvas.state = [[' ' for _ in range(self.canvas.width)] for _ in range(self.canvas.height)]
    
    def validate(self, input: list[str]) -> bool:
        return True
    
    def get_help_text(self) -> str:
        return(
            "                                         |  Clear the canvas\n"
        )
    

class UndoCommand(Command):
    def execute(self, input: list[str]):
        last_changes = self.history_stack.undo_stack.pop()
        if last_changes:
            for x,y,old_char, new_char in last_changes:
                self.canvas.state[y][x] = old_char
        
        self.history_stack.add_to_redo(last_changes)
    
    def validate(self, input: list[str]) -> bool:
        if len(input)>1:
            print("Too many arguments. Ignoring extra characters")
        
        return True
    
    def get_help_text(self) -> str:
        return(
            "                                         |  Undo the last command\n"
        )