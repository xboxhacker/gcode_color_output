import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import random

# List of colors to use (excluding #000080)
colors = [
    "#00ffff", "#0000ff", "#ff00ff", "#009900", 
    "#990000", "#808000", "#ff0000", "#800080"
]

selected_type = None
search_start = "1.0"

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

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".gcode",
                                             filetypes=[("G-code files", "*.gcode"), ("All files", "*.*")])
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text_widget.get("1.0", tk.END))

def display_gcode(processed_gcode):
    text_widget.config(state=tk.NORMAL)
    text_widget.delete('1.0', tk.END)
    for line, color in processed_gcode:
        if color:
            text_widget.insert(tk.END, line, color)
            text_widget.tag_config(color, foreground=color)
        else:
            text_widget.insert(tk.END, line)
    text_widget.config(state=tk.NORMAL)  # Allow editing

def display_types(color_map):
    type_listbox.delete(0, tk.END)
    for section_type, color in color_map.items():
        type_listbox.insert(tk.END, section_type)
        type_listbox.itemconfig(tk.END, {'bg': color})

def lighten_color(hex_color, factor=0.7):
    """Lightens the given color by multiplying (1-luminosity) by the given factor (0.7 for 30% transparency)."""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    lighter_rgb = tuple(int(x + (255 - x) * factor) for x in rgb)
    return '#{:02x}{:02x}{:02x}'.format(*lighter_rgb)

def on_type_select(event):
    global selected_type, search_start
    selected_index = type_listbox.curselection()
    if selected_index:
        selected_type = type_listbox.get(selected_index)
        color = type_listbox.itemcget(selected_index, 'bg')
        highlight_color = lighten_color(color)
        
        # Remove previous highlights
        text_widget.tag_remove('highlight', '1.0', tk.END)
        
        # Highlight all sections with the selected type
        start = '1.0'
        while True:
            pos = text_widget.search(selected_type, start, stopindex=tk.END, nocase=True)
            if not pos:
                break
            # Find the end of the section
            line_num = int(pos.split('.')[0])
            end_pos = f"{line_num + 1}.0"
            while True:
                next_line_start = text_widget.search(';TYPE:', end_pos, stopindex=tk.END, nocase=True)
                if not next_line_start or int(next_line_start.split('.')[0]) > line_num + 1:
                    end_pos = next_line_start if next_line_start else tk.END
                    break
                line_num += 1
                end_pos = f"{line_num + 1}.0"
            
            text_widget.tag_add('highlight', pos, end_pos)
            start = end_pos
        
        text_widget.tag_config('highlight', background=highlight_color)
        search_start = "1.0"

def next_section():
    global search_start
    if selected_type:
        pos = text_widget.search(selected_type, search_start, stopindex=tk.END, nocase=True)
        if pos:
            text_widget.see(pos)
            search_start = f"{int(pos.split('.')[0]) + 1}.0"

def main():
    global text_widget, type_listbox
    root = tk.Tk()
    root.title("G-code Processor")
    root.resizable(True, True)  # Allow the window to be resizable

    open_button = tk.Button(root, text="Open G-code File", command=open_file)
    open_button.pack(pady=10)

    save_button = tk.Button(root, text="Save As", command=save_file)
    save_button.pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(pady=10, expand=True, fill=tk.BOTH)

    text_widget = ScrolledText(frame, wrap=tk.WORD, height=25, width=100)
    text_widget.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
    text_widget.config(state=tk.DISABLED)

    right_frame = tk.Frame(frame)
    right_frame.pack(side=tk.RIGHT, fill=tk.Y)

    next_button = tk.Button(right_frame, text="Next Section", command=next_section)
    next_button.pack(pady=10)

    type_listbox = tk.Listbox(right_frame, width=30)
    type_listbox.pack(fill=tk.Y)
    type_listbox.bind('<<ListboxSelect>>', on_type_select)

    root.mainloop()

if __name__ == "__main__":
    main()
