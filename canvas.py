class Canvas:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.state = None
            self.width = None
            self.height = None

    def initialize_canvas(self, width: int, height: int):
        """Initialize canvas with given dimensions."""
        if not isinstance(width, int) or not isinstance(height, int):
            print("Width and height must be integers")
            return
        if width <= 0 or height <= 0:
            print("Width and height must be positive integers")
            return
        if self.state is not None:
            print("Canvas already exists. Clear Canvas first to start a new one.")
            return
        self.state = [[' ' for _ in range(width)] for _ in range(height)]
        self.width = width
        self.height = height
        self._initialized = True   
    
    def print_canvas(self):
        print('-' * (self.width + 2))
        for row in reversed(self.state):
            print('|' + ''.join(str(cell) for cell in row) + '|')
        print('-' * (self.width + 2))
        
    
    def validate_coordinates(self, x1: int, y1: int, x2: int = None, y2: int = None):
        if x2 is not None and y2 is not None:
            if (x1 < 0 or x1 >= self.width or y1 < 0 or y1 >= self.height or 
                x2 < 0 or x2 >= self.width or y2 < 0 or y2 >= self.height):
                return False
        else:
            if x1 < 0 or x1 >= self.width or y1 < 0 or y1 >= self.height:
                return False
        return True