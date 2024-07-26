import tkinter as tk
from tkinter import filedialog
import os
import pywintypes
import win32api


def select_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("Python Files", "*.py")])
    if file_path:
        entry_file.delete(0, tk.END)
        entry_file.insert(0, file_path)


def select_icon():
    icon_path = filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")])
    if icon_path:
        entry_icon.delete(0, tk.END)
        entry_icon.insert(0, icon_path)


def select_output_dir():
    output_dir = filedialog.askdirectory()
    if output_dir:
        entry_output_dir.delete(0, tk.END)
        entry_output_dir.insert(0, output_dir)


def convert_to_exe():
    py_file = entry_file.get()
    if not py_file.endswith(".py"):
        status_label.config(text="Please select a Python file (.py)", fg="red")
        return

    output_dir = entry_output_dir.get()
    output_name = os.path.splitext(os.path.basename(py_file))[
        0]  # Use input file name

    options = []

    if var_onefile.get():
        options.append("--onefile")
    if var_noconsole.get():
        options.append("--noconsole")
    if entry_icon.get():
        options.append("--icon=" + entry_icon.get())
    if var_clean.get():
        options.append("--clean")

    # Construct the command string
    options_str = " ".join(options)
    command = f"pyinstaller {options_str} {py_file}"
    print(command)

    # Change directory to the output directory
    os.chdir(output_dir)

    # Execute the command
    os.system(command)

    # Change back to the original directory
    os.chdir(os.path.dirname(__file__))

    status_label.config(text="Conversion completed!", fg="green")


# Create the main window
root = tk.Tk()
root.title("Py to Exe Converter")
root.geometry("510x290")
# root.iconbitmap('pxe.ico')

label_title = tk.Label(root, text=".PY to .EXE Converter",
                       font=("Arial", 16, "bold"))
label_title.grid(row=0, column=0, padx=(60, 0), columnspan=10, pady=13)


# File Selection
label_file = tk.Label(root, text="Select Python File:")
label_file.grid(row=1, column=0, padx=5, pady=5, sticky="w")

entry_file = tk.Entry(root, width=50)
entry_file.grid(row=1, column=1, padx=5, pady=5)

button_browse = tk.Button(root, text="Browse", command=select_file)
button_browse.grid(row=1, column=2, padx=5, pady=5)

# Output Directory
label_output_dir = tk.Label(root, text="Output Directory:")
label_output_dir.grid(row=2, column=0, padx=5, pady=5, sticky="w")

entry_output_dir = tk.Entry(root, width=50)
entry_output_dir.grid(row=2, column=1, padx=5, pady=5)

button_output_dir = tk.Button(root, text="Browse", command=select_output_dir)
button_output_dir.grid(row=2, column=2, padx=5, pady=5)

# Options
var_onefile = tk.BooleanVar(value=True)
check_onefile = tk.Checkbutton(root, text="One File", variable=var_onefile)
check_onefile.grid(row=4, column=1, padx=5, pady=5, sticky="w")

var_noconsole = tk.BooleanVar()
check_noconsole = tk.Checkbutton(
    root, text="No Console", variable=var_noconsole)
check_noconsole.grid(row=4, column=1, padx=(220, 0), pady=5, sticky="w")

var_clean = tk.BooleanVar(value=True)
check_clean = tk.Checkbutton(root, text="Clean Build", variable=var_clean)
check_clean.grid(row=4, column=1, padx=(110, 0), pady=5, sticky="w")

# Icon Selection
label_icon = tk.Label(root, text="Select Icon File:")
label_icon.grid(row=3, column=0, padx=5, pady=5, sticky="w")

entry_icon = tk.Entry(root, width=50)
entry_icon.grid(row=3, column=1, padx=5, pady=5)

button_icon = tk.Button(root, text="Browse", command=select_icon)
button_icon.grid(row=3, column=2, padx=5, pady=5)

# Conversion Button
button_convert = tk.Button(
    root, text="Convert to .exe", command=convert_to_exe)
button_convert.grid(row=5, column=1, padx=5, pady=10)

# Status Label
status_label = tk.Label(root, text="", fg="green")
status_label.grid(row=6, column=1, padx=5, pady=5)

root.mainloop()
