import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, colorchooser
from PIL import Image, ImageTk  # Make sure you have Pillow installed

class TexEdit:
    def __init__(self, root):
        self.root = root
        self.root.title("TexEdit")
        
        # Load and set the icon
        self.set_icon("TexEdit.png")  # Ensure this is the path to your PNG icon
        
        self.create_widgets()

    def set_icon(self, icon_path):
        try:
            icon = Image.open(icon_path)
            icon = ImageTk.PhotoImage(icon)
            self.root.iconphoto(True, icon)
        except Exception as e:
            print(f"Error setting icon: {e}")

    def create_widgets(self):
        self.text = tk.Text(self.root, wrap='word', undo=True)
        self.text.pack(fill='both', expand=True)

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.edit_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", command=self.select_all)
        self.edit_menu.add_command(label="Find", command=self.find_text)
        self.edit_menu.add_command(label="Replace", command=self.replace_text)

        self.format_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Font...", command=self.change_font)
        self.format_menu.add_command(label="Color...", command=self.change_color)

        self.help_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filepath:
            with open(filepath, 'r') as file:
                content = file.read()
                self.text.delete('1.0', tk.END)
                self.text.insert('1.0', content)
                self.root.title(f"TexEdit - {filepath}")

    def save_file(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filepath:
            with open(filepath, 'w') as file:
                content = self.text.get('1.0', tk.END)
                file.write(content)
                self.root.title(f"TexEdit - {filepath}")

    def cut_text(self):
        self.text.event_generate('<<Cut>>')

    def copy_text(self):
        self.text.event_generate('<<Copy>>')

    def paste_text(self):
        self.text.event_generate('<<Paste>>')

    def select_all(self):
        self.text.tag_add('sel', '1.0', tk.END)

    def find_text(self):
        find_str = simpledialog.askstring("Find", "Enter text to find:")
        if find_str:
            self.highlight_text(find_str)

    def replace_text(self):
        find_str = simpledialog.askstring("Find", "Enter text to find:")
        replace_str = simpledialog.askstring("Replace", "Enter replacement text:")
        if find_str is not None and replace_str is not None:
            content = self.text.get('1.0', tk.END)
            new_content = content.replace(find_str, replace_str)
            self.text.delete('1.0', tk.END)
            self.text.insert('1.0', new_content)

    def highlight_text(self, text):
        self.text.tag_remove('highlight', '1.0', tk.END)
        start_idx = '1.0'
        while True:
            start_idx = self.text.search(text, start_idx, nocase=True, stopindex=tk.END)
            if not start_idx:
                break
            end_idx = f"{start_idx}+{len(text)}c"
            self.text.tag_add('highlight', start_idx, end_idx)
            self.text.tag_config('highlight', background='yellow')
            start_idx = end_idx

    def change_font(self):
        font_name = simpledialog.askstring("Font", "Enter font name (e.g., Arial):")
        font_size = simpledialog.askinteger("Font Size", "Enter font size:")
        if font_name and font_size:
            self.text.config(font=(font_name, font_size))

    def change_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text.config(fg=color)

    def show_about(self):
        messagebox.showinfo("About", "TexEdit v1.0\nCreated with Tkinter, a Python preinstall plugin for GUI's also used in this application.")

if __name__ == "__main__":
    root = tk.Tk()
    editor = TexEdit(root)
    root.mainloop()
