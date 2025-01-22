# G-code Color Output
Simple python script to take a 3d printing gcode file and colorize the printing sections. This will make it a little easier to read and edit the gcode file. ie. Inner wall, outter wall ... etc.

## Features

- Open and process G-code files.
- Color-code different `;TYPE:` sections. <~ OrcaSlicer output
- Display the G-code in a resizable window.
- List `;TYPE:` sections with their colors for easy reference.
- Highlights every `;TYPE:` section when picked from list list box.
- Next Section button jumps the output window to the next highlighted section.

## Requirements

- Python 3.x

## Installation

1. Clone the repository or download the script.
2. Ensure you have Python 3.x installed on your machine.

## Usage

1. Run the script using Python:

    ```bash
    python gcode_processor.py
    ```

2. Click the "Open G-code File" button to open a `.gcode` file.
3. The processed G-code with color-coded `;TYPE:` sections will be displayed in the text area.
4. The `;TYPE:` sections and their corresponding colors will be listed on the right.

