# Console Drawing Tool

A command-line drawing tool that allows users to create shapes and fill areas on a canvas.

## Features

- Create a canvas of specified dimensions
- Draw lines (horizontal, vertical, and diagonal)
- Draw rectangles
- Fill areas with bucket fill
- Clear canvas
- Interactive command-line interface

## Commands

| Command | Description | Example |
|---------|-------------|---------|
| `C` | Create a new canvas | `C 20 4` |
| `L` | Draw a line | `L 1 2 6 2 x` |
| `R` | Draw a rectangle | `R 14 1 18 3 o` |
| `B` | Fill an area | `B 10 3 o` |
| `Q` | Quit the program | `Q` |
|---------------------------------|
|Additional Commands Implemented|
| `E` | Clear the canvas | `E` |

## Assumptions

1. **Canvas Coordinates**:
   - Zero-based indexing (starts from 0)
   - (0,0) is at the bottom-left corner (when printed on console)
   - X increases from left to right
   - Y increases from bottom to top

2. **Input Validation**:
   - All coordinates must be integers
   - Coordinates must be within canvas bounds
   - Character input must be a single character

3. **Drawing Rules**:
   - Lines can be horizontal, vertical, or diagonal
   - Rectangles must have different x and y coordinates for corners
   - BucketFill command functions like bucket tool in classic applications like paint:
     - Boundary Filling: When applied to a boundary point, only the boundary itself changes color.
     - Shape Filling: When applied inside a closed shape (such as a rectangle), the entire enclosed area is filled with the selected color.
     - Complex Shape Handling: When applied inside an area enclosed by multiple boundary types (identified by different values in the canvas), the entire enclosed region is filled regardless of the boundary composition.

4. **Canvas Behavior**:
   - Canvas is a singleton (only one instance exists)
   - Canvas must be created before drawing
   - Canvas can be cleared and recreated

## Running Program

Draw.exe is added to the root directory for easily running the program. 
Generated using pyinstaller

## Cloning and Manual Running

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the program:
```bash
python main.py
```

## Error Handling

The program handles various error cases including but not limited to:
- Invalid coordinates
- Missing canvas
- Invalid command syntax
- Out-of-bounds drawing
- Invalid character input

## Development

- Python 3.12+
- No external dependencies required
- Uses standard library modules

## Testing

Run tests using:
```bash
python -m unittest discover tests
```

## Author

Rishabh Nautiyal