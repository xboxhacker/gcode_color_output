import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import random

# List of colors to use (excluding white and black)
colors = [
    "#FF5733", "#33FF57", "#3357FF", "#F0E68C", "#8A2BE2", "#FF6347", 
    "#4682B4", "#D2691E", "#9ACD32", "#DDA0DD", "#FF4500", "#2E8B57"
]

def process_gcode(file_path):
    with open(file_path, 'r') as file:
        gcode_lines = file.readlines()

    output_lines = []
    color_map = {}
    used_colors = set()
    current_color = None

    for line in gcode_lines:
        if line.startswith(';TYPE:'):
            section_type = line.strip()
            if section_type not in color_map:
                # Select a random color that hasn't been used yet
                available_colors = [color for color in colors if color not in used_colors]
                if not available_colors:
                    available_colors = colors  # Reset if all colors have been used
                    used_colors = set()
                selected_color = random.choice(available_colors)
                used_colors.add(selected_color)
                color_map[section_type] = selected_color
            current_color = color_map[section_type]
        output_lines.append((line, current_color))

    return output_lines, color_map

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("G-code files", "*.gcode"), ("All files", "*.*")])
    if file_path:
        processed_gcode, color_map = process_gcode(file_path)
        display_gcode(processed_gcode)
        display_types(color_map)

def display_gcode(processed_gcode):
    text_widget.config(state=tk.NORMAL)
    text_widget.delete('1.0', tk.END)
    for line, color in processed_gcode:
        if color:
            text_widget.insert(tk.END, line, color)
            text_widget.tag_config(color, foreground=color)
        else:
            text_widget.insert(tk.END, line)
    text_widget.config(state=tk.DISABLED)

def display_types(color_map):
    type_listbox.delete(0, tk.END)
    for section_type, color in color_map.items():
        type_listbox.insert(tk.END, section_type)
        type_listbox.itemconfig(tk.END, {'bg': color})

def main():
    global text_widget, type_listbox
    root = tk.Tk()
    root.title("G-code Processor")
    root.resizable(True, True)  # Allow the window to be resizable

    open_button = tk.Button(root, text="Open G-code File", command=open_file)
    open_button.pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=10, expand=True, fill=tk.BOTH)

    text_widget = ScrolledText(frame, wrap=tk.WORD, height=25, width=100)
    text_widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    text_widget.config(state=tk.DISABLED)

    type_listbox = tk.Listbox(frame, width=30)
    type_listbox.pack(side=tk.RIGHT, fill=tk.Y)

    root.mainloop()

if __name__ == "__main__":
    main()
