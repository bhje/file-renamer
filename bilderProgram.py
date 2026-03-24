import os
import csv
from natsort import natsorted
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
from tkinterdnd2 import DND_FILES, TkinterDnD
import shutil

# Root window
root = TkinterDnD.Tk()
root.title("File renamer")
root.geometry("1024x640")

# Style
style = ttk.Style()

style.theme_use('clam')

style.map("TButton",
          foreground=[('pressed', 'white'), ('active', 'black')],
          background=[('pressed', '!disabled', '#347083'), ('active', '#347083')]
            )
style.configure("TButton",
                font=("Roboto", 10),
                foreground="black")
style.map("R.TButton",
          foreground=[('pressed', 'white'), ('active', 'black')],
          background=[('pressed', '#EB091C'), ('active', '#EB091C')]
            )
style.configure("R.TButton",
                font=("Roboto", 10),
                foreground="black")

style.configure("Treeview", background="#ADBBC4", foreground="black", rowheight=25, fieldbackground="#ADBBC4")
style.map('Treeview', background=[('selected', '#347083')])

def run_renamer(csv_path_entry, images_folder_entry, output_folder_entry):
    csv_path = csv_path_entry.get().strip()
    images_folder = images_folder_entry.get().strip()
    output_folder = output_folder_entry.get().strip()

    col_idx_new = h4.current()
    
    if col_idx_new < 0:
        messagebox.showwarning("Warning", "Please select columns for new names.")
        return

    try:
        # Create output folder if one does not exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with open(csv_path, mode='r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)

        count = 0

        dir_list = os.listdir(images_folder)
        sortedlist = natsorted(dir_list)

        for index, row in enumerate(data[1:], start=1):
            if index > len(sortedlist):
                print(f"Index {index} exceeds the number of files in the images folder. Stopping process.")
                break
            
            try:
                target_filename = row[col_idx_new]

                if not target_filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
                    target_filename += os.path.splitext(sortedlist[index-1])[1]

                old_filename = sortedlist[index-1]

                src = os.path.join(images_folder, old_filename)
                dst = os.path.join(output_folder, target_filename)
                
                if images_folder != output_folder:
                    shutil.copy2(src, dst)
                else:
                    os.rename(src, dst)
    
                count += 1

            except IndexError:
                continue

        messagebox.showinfo("Done!", f"The process has completed. \n{count} photos were renamed.")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: \n{str(e)}")

# Reset function
def reset_all():
    entry_csv.delete(0, tk.END)
    entry_img.delete(0, tk.END)
    entry_out.delete(0, tk.END)
    h4.set("New name (Choose column)")
    update_table()

    for row in recipe_tab.winfo_children()[1:]:
        row.destroy()

    for row in tree.get_children():
        tree.delete(row)

    for label in options_tab.winfo_children()[1:]:
        label.destroy()

# Filechoosers
def select_csv():
    path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry_csv.delete(0, tk.END)
    entry_csv.insert(0, path)

    csv_to_table(path, tree)

def select_in_folder():
    path = filedialog.askdirectory()
    entry_img.delete(0, tk.END)
    entry_img.insert(0, path)

    img_to_table(path, tree)

def select_out_folder():
    path = filedialog.askdirectory()
    entry_out.delete(0, tk.END)
    entry_out.insert(0, path)

def start_process():
    csv = entry_csv
    img = entry_img
    out = entry_out

    if csv and img and out:
        run_renamer(csv, img, out)
    else:
        messagebox.showwarning("Warning", "Please choose all paths.")

# Load table with data
def load_table(csv_data, img_data, tree, col_idx_new = 1):
    for item in tree.get_children():
        tree.delete(item)

    if h4.get() == "New name (Choose column)":
        col_idx_new = 1

    file_list = []
    if img_data and os.path.exists(img_data):
        try:
            files = os.listdir(img_data)
            sorted_files = natsorted(files)
            file_list = sorted_files
        except Exception:
            file_list = []

    csv_rows = csv_data[1:] if csv_data else []
    max_rows = max(len(csv_rows), len(file_list))

    for i in range(max_rows):
        file_num = str(i + 1)
        
        if i < len(file_list):
            curr_name = file_list[i]
        else:
            curr_name = "No file data"

        if i < len(csv_rows):
            try:
                row = csv_rows[i]
                new_name = row[col_idx_new] if col_idx_new < len(row) else ""
            except IndexError:
                new_name = "Something wrong with the csv data"
        else:
            new_name = "No csv data"

        tree.insert("", "end", values=(file_num, curr_name, new_name))

# Load table from csv path
def csv_to_table(csv_path, tree):
    try:
        with open(csv_path, mode = 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {csv_path}")
    
    update_dropdowns(data)
    update_table()

    print("Table loaded with new csv data.")

# Load table from image folder path
def img_to_table(folder_path, tree):
    try:
        files = os.listdir(folder_path)
        sorted_files = natsorted(files)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Folder not found: {folder_path}")
    
    data = [["Current name"]]
    for file in sorted_files:
        data.append([file])

    update_table()

    print("Table loaded with new folder data.")

# Load table from drag and drop
def drop(event):
    file_path = event.data
    if file_path.endswith('.csv'):
        print("Dropped csv-file: ", file_path)
        entry_csv.delete(0, tk.END)
        entry_csv.insert(0, file_path)
        csv_to_table(file_path, tree)
    elif os.path.isdir(file_path):
        print("Dropped folder: ", file_path)
        if not os.listdir(file_path):
            entry_out.delete(0, tk.END)
            entry_out.insert(0, file_path)
        else: 
            entry_img.delete(0, tk.END)
            entry_img.insert(0, file_path)
            img_to_table(file_path, tree)
            if not entry_out.get():
                entry_out.delete(0, tk.END)
                entry_out.insert(0, file_path)
                messagebox.showinfo("Info", "Output folder set to the same as input folder since no output folder was chosen.")
    else:
        messagebox.showerror("Error", "Please drop a CSV file or an image folder.")

# Apply serialize function to table
def apply_serialize(start_num, increment):
    for item in tree.get_children():
        index = tree.item(item, "values")[0]
        current_name = tree.item(item, "values")[2]
        new_name = f"{current_name}{start_num + (int(index) - 1) * increment}"
        tree.set(item, column="new_name", value=new_name)

# Apply insert function to table
def apply_insert(text, position):
    for item in tree.get_children():
        current_name = tree.item(item, "values")[2]
        if position == "start":
            new_name = text + current_name
        elif position == "end":
            new_name = current_name + text
        else:
            new_name = current_name
        tree.set(item, column="new_name", value=new_name)

# Apply remove function to table
def apply_remove(text):
    if not text:
        for item in tree.get_children():
            current_name = tree.item(item, "values")[2]
            tree.set(item, column="new_name", value="")
        return
    for item in tree.get_children():
        current_name = tree.item(item, "values")[2]
        new_name = current_name.replace(text, "")
        tree.set(item, column="new_name", value=new_name)

# Apply replace function to table
def apply_replace(find_text, replace_text):
    for item in tree.get_children():
        current_name = tree.item(item, "values")[2]
        new_name = current_name.replace(find_text, replace_text)
        tree.set(item, column="new_name", value=new_name)

# Column names to drop-downs
def update_dropdowns(data):
    columns = data[0]
    h4['values'] = columns

# Update table when drop-down selection changes
def update_table(event=None):
    new_idx = h4.current()

    if new_idx < 0: new_idx = 1
    csv_path = entry_csv.get()
    folder_path = entry_img.get()

    csv_data = []

    if csv_path and os.path.exists(csv_path):
        try:
            with open(csv_path, mode = 'r', encoding='utf-8', newline='') as file:
                reader = csv.reader(file)
                csv_data = list(reader)
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {csv_path}")
        
    load_table(csv_data, folder_path, tree, new_idx)

# Recipe line removal
def delete_step(recipe_widget, options_widget):
    recipe_widget.destroy()
    options_widget.destroy()

# Functions for functions
def add_serialize_ui():
    recipe_button = ttk.Button(recipe_tab, text="Serialize", style="R.TButton", command=lambda: delete_step(recipe_button, ui_frame))
    recipe_button.pack(fill='x', padx=5, pady=2)

    ui_frame = tk.Frame(options_tab, height=50, bg="#A8B9C4")
    ui_frame.pack(fill='x')

    tk.Label(ui_frame, text="Serialize options:", bg="#A8B9C4", font=("Roboto", 10, "bold")).pack(padx=5, pady=(10, 2), anchor='nw', side='left')
    tk.Label(ui_frame, text="Start number", bg="#A8B9C4").pack(padx=5, pady=(10, 2), anchor='nw', side='left')
    tk.Entry(ui_frame, width=20).pack(padx=5, pady=(10, 2), anchor='nw', side='left')
    tk.Label(ui_frame, text="Increment", bg="#A8B9C4").pack(padx=5, pady=(10, 2), anchor='nw', side='left')
    tk.Entry(ui_frame, width=20).pack(padx=5, pady=(10, 2), anchor='nw', side='left')

def add_insert_ui():
    recipe_button = ttk.Button(recipe_tab, text="Insert", style="R.TButton", command=lambda: delete_step(recipe_button, ui_frame))
    recipe_button.pack(fill='x', padx=5, pady=2)

    ui_frame = tk.Frame(options_tab, height=50, bg="#A8B9C4")
    ui_frame.pack(fill='x')

    tk.Label(ui_frame, text="Insert options:", bg="#A8B9C4", font=("Roboto", 10, "bold")).pack(padx=5, pady=(10, 2), anchor='nw', side='left')
    tk.Label(ui_frame, text="Text to insert", bg="#A8B9C4").pack(padx=5, pady=(10, 2), anchor='nw', side='left')
    tk.Entry(ui_frame, width=20).pack(padx=5, pady=(10, 2), anchor='nw', side='left')
    tk.Label(ui_frame, text="Position", bg="#A8B9C4").pack(padx=5, pady=(10, 2), anchor='nw', side='left')
    position_var = tk.StringVar(value="start")
    tk.Radiobutton(ui_frame, text="Start", variable=position_var, value="start", bg="#A8B9C4").pack(pady=(10, 2), anchor='nw', side='left')
    tk.Radiobutton(ui_frame, text="End", variable=position_var, value="end", bg="#A8B9C4").pack(pady=(10, 2), anchor='nw', side='left')
    tk.Radiobutton(ui_frame, text="Choose:", variable=position_var, value="choose", bg="#A8B9C4").pack(pady=(10, 2), anchor='nw', side='left')
    choose_entry = tk.Entry(ui_frame, width=2)
    choose_entry.pack(padx=5, pady=(10, 2), anchor='nw', side='left')

def add_remove_ui():
    recipe_button = ttk.Button(recipe_tab, text="Remove", style="R.TButton", command=lambda: delete_step(recipe_button, ui_frame))
    recipe_button.pack(fill='x', padx=5, pady=2)

    ui_frame = tk.Frame(options_tab, height=50, bg="#A8B9C4")
    ui_frame.pack(fill='x')

    text_var = tk.StringVar()
    remove_all_var = tk.BooleanVar(value=False)

    def uncheck_all(*args):
        if text_var.get():
            remove_all_var.set(False)

    def clear_text():
        text_var.set("")

    text_var.trace_add("write", uncheck_all)

    tk.Label(ui_frame, text="Remove options:", bg="#A8B9C4", font=("Roboto", 10, "bold")).pack(padx=5, pady=(10, 2), anchor='nw', side='left')
    tk.Label(ui_frame, text="Text to remove", bg="#A8B9C4").pack(padx=5, pady=(10, 2), anchor='nw', side='left')
    tk.Entry(ui_frame, width=20, textvariable=text_var).pack(padx=5, pady=(10, 2), anchor='nw', side='left')
    tk.Label(ui_frame, text="Remove all", bg="#A8B9C4").pack(padx=5, pady=(10, 2), anchor='nw', side='left')
    tk.Radiobutton(ui_frame, text="Yes", variable=remove_all_var, value=True, bg="#A8B9C4", command=clear_text).pack(pady=(10, 2), anchor='nw', side='left')

def add_replace_ui():
    recipe_button = ttk.Button(recipe_tab, text="Replace", style="R.TButton", command=lambda: delete_step(recipe_button, ui_frame))
    recipe_button.pack(fill='x', padx=5, pady=2)

    ui_frame = tk.Frame(options_tab, height=50, bg="#A8B9C4")
    ui_frame.pack(fill='x')

    tk.Label(ui_frame, text="Replace options:", bg="#A8B9C4", font=("Roboto", 10, "bold")).pack(padx=5, pady=(10, 2), anchor='nw', side='left')
    tk.Label(ui_frame, text="Text to replace", bg="#A8B9C4").pack(padx=5, pady=(10, 2), anchor='nw', side='left')
    tk.Entry(ui_frame, width=20).pack(padx=5, pady=(10, 2), anchor='nw', side='left')
    tk.Label(ui_frame, text="Replacement text", bg="#A8B9C4").pack(padx=5, pady=(10, 2), anchor='nw', side='left')
    tk.Entry(ui_frame, width=20).pack(padx=5, pady=(10, 2), anchor='nw', side='left')

# Menubar
menubar = Menu(root)

# Menubar file button
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu = file)
file.add_command(label = 'Choose Input Folder', command=select_in_folder)
file.add_command(label = 'Choose Output Folder', command=select_out_folder)
file.add_command(label = 'Choose CSV', command=select_csv)

# Menubar function button
function = Menu(menubar, tearoff=0)
menubar.add_cascade(label='Function', menu = function)
function.add_command(label='Serialize', command=lambda: open_serialize_window())
function.add_command(label='Insert', command=lambda: open_insert_window())
function.add_command(label='Remove', command=lambda: open_remove_window())
function.add_command(label='Replace', command=lambda: open_replace_window())

# Show CSV window
def show_csv_window():
    functions_frame.pack_forget()
    csv_frame.pack(expand=True, fill='both')
    switch_button_c.grid_remove()
    switch_button_f.grid()

# Functions window
def show_functions_window():
    csv_frame.pack_forget()
    functions_frame.pack(expand=True, fill='both')
    switch_button_f.grid_remove()
    switch_button_c.grid()

# Serialize window
def open_serialize_window():
    serialize_window = tk.Toplevel(root)
    serialize_window.title("Serialize")
    serialize_window.geometry("600x400")

    tk.Label(serialize_window, text="Start number:").pack(pady=10)
    start_entry = tk.Entry(serialize_window, width=30)
    start_entry.pack(pady=5)

    tk.Label(serialize_window, text="Increment:").pack(pady=10)
    increment_entry = tk.Entry(serialize_window, width=30)
    increment_entry.pack(pady=5)

    tk.Button(serialize_window, text="Apply", command=lambda: apply_serialize(int(start_entry.get()), int(increment_entry.get()))).pack(pady=20)

# Insert window
def open_insert_window():
    insert_window = tk.Toplevel(root)
    insert_window.title("Insert")
    insert_window.geometry("600x400")

    tk.Label(insert_window, text="Text to insert:").pack(pady=10)
    text_entry = tk.Entry(insert_window, width=30)
    text_entry.pack(pady=5)
    tk.Label(insert_window, text="Position:").pack(pady=10)

    position_var = tk.StringVar(value="start")
    tk.Radiobutton(insert_window, text="Start", variable=position_var, value="start").pack(pady=5)
    tk.Radiobutton(insert_window, text="End", variable=position_var, value="end").pack(pady=5)

    tk.Button(insert_window, text="Apply", command=lambda: apply_insert(text_entry.get(), position_var.get())).pack(pady=20)

# Remove window
def open_remove_window():
    remove_window = tk.Toplevel(root)
    remove_window.title("Remove")
    remove_window.geometry("600x400")
    
    tk.Label(remove_window, text="Text to remove:").pack(pady=10)
    text_entry = tk.Entry(remove_window, width=30)
    text_entry.pack(pady=5)

    tk.Button(remove_window, text="Apply", command=lambda: apply_remove(text_entry.get())).pack(pady=20)

# Replace window
def open_replace_window():
    replace_window = tk.Toplevel(root)
    replace_window.title("Replace")
    replace_window.geometry("600x400")

    find_label = tk.Label(replace_window, text="Find:")
    find_label.pack(pady=10)
    find_entry = tk.Entry(replace_window, width=30)
    find_entry.pack(pady=5)

    replace_label = tk.Label(replace_window, text="Replace with:")
    replace_label.pack(pady=10)
    replace_entry = tk.Entry(replace_window, width=30)
    replace_entry.pack(pady=5)

    tk.Button(replace_window, text="Apply", command=lambda: apply_replace(find_entry.get(), replace_entry.get())).pack(pady=20)

def apply_all_functions():
    for ui_frame in options_tab.winfo_children()[1:]:
        for widget in ui_frame.winfo_children():
            if isinstance(widget, tk.Label) and "Serialize options:" in widget.cget("text"):
                entries = [w for w in ui_frame.winfo_children() if isinstance(w, tk.Entry)]
                if len(entries) >= 2:
                    try:
                        start_num = int(entries[0].get())
                        increment = int(entries[1].get())
                        apply_serialize(start_num, increment)
                        print("Applied serialize function.")
                    except ValueError:
                        messagebox.showerror("Error", "Please enter valid numbers for serialize function.")
            elif isinstance(widget, tk.Label) and "Insert options:" in widget.cget("text"):
                text_entry = next((w for w in ui_frame.winfo_children() if isinstance(w, tk.Entry)), None)
                position_var = next((w for w in ui_frame.winfo_children() if isinstance(w, tk.Radiobutton)), None)
                if text_entry and position_var:
                    apply_insert(text_entry.get(), position_var.cget("value"))
                print("Applied insert function.")
            elif isinstance(widget, tk.Label) and "Remove options:" in widget.cget("text"):
                text_entry = next((w for w in ui_frame.winfo_children() if isinstance(w, tk.Entry)), None)
                remove_all_var = next((w for w in ui_frame.winfo_children() if isinstance(w, tk.Checkbutton)), None)
                if text_entry:
                    apply_remove(text_entry.get())
                elif remove_all_var and remove_all_var.var.get():
                    apply_remove("")
                print("Applied remove function.")
            elif isinstance(widget, tk.Label) and "Replace options:" in widget.cget("text"):
                entries = [w for w in ui_frame.winfo_children() if isinstance(w, tk.Entry)]
                if len(entries) >= 2:
                    apply_replace(entries[0].get(), entries[1].get())
                print("Applied replace function.")

def sort_name_by(tv):
    by = h3.get()
    if by == "Name":
        l = [(tv.set(k, "current_name"), k) for k in tv.get_children('')]
        l.sort(key=lambda t: t[0])

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
    elif by == "Last modified":
        sorted_items = sorted(tv.get_children(''), key=lambda k: os.path.getmtime(os.path.join(entry_img.get(), tv.set(k, "current_name"))))
        for index, k in enumerate(sorted_items):
            tv.move(k, '', index)
    elif by == "Created":
        sorted_items = sorted(tv.get_children(''), key=lambda k: os.path.getctime(os.path.join(entry_img.get(), tv.set(k, "current_name"))))
        for index, k in enumerate(sorted_items):
            tv.move(k, '', index)
    else:
        return

# Upper Frame
upper_frame = tk.Frame(root, height=250, bg="#F0F0F0")
upper_frame.pack(side=tk.TOP, fill=tk.X)
upper_frame.pack_propagate(False)

# Functions frame
functions_frame = tk.Frame(upper_frame, height=250, bg="#F0F0F0", padx=10)
functions_frame.pack_propagate(False)

# Functions tab
functions_tab = tk.Frame(functions_frame, bg="#AD8EB6", width=200)
functions_tab.pack(fill='y', side='left', padx=(0, 5))
functions_tab.pack_propagate(False)

functions_label = tk.Label(functions_tab, text="Functions", bg="#AD8EB6", font=("Roboto", 12, "bold"))
functions_label.pack(padx = 5, pady=5, side='top', anchor='w')

# Function buttons
ttk.Button(functions_tab, text="Serialize", width=30, command=lambda: add_serialize_ui(), style = "TButton").pack(pady=5, padx=10, anchor='w')
ttk.Button(functions_tab, text="Insert", width=30, command=lambda: add_insert_ui(), style = "TButton").pack(pady=5, padx=10, anchor='w')
ttk.Button(functions_tab, text="Remove", width=30, command=lambda: add_remove_ui(), style = "TButton").pack(pady=5, padx=10, anchor='w')
ttk.Button(functions_tab, text="Replace", width=30, command=lambda: add_replace_ui(), style = "TButton").pack(pady=5, padx=10, anchor='w')

# Recipe tab
recipe_tab = tk.Frame(functions_frame, bg="#BBD8AD", width=200)
recipe_tab.pack(padx=(0, 5), fill='y', side='left')
recipe_tab.pack_propagate(False)

recipe_label = tk.Label(recipe_tab, text="Recipe", bg="#BBD8AD", font=("Roboto", 12, "bold"))
recipe_label.pack(padx = 5, pady=5, side='top', anchor='w')

# Options tab
options_tab = tk.Frame(functions_frame, bg="#B6C5CF")
options_tab.pack(expand=True, fill='both', side='left')
options_tab.pack_propagate(False)

options_label = tk.Label(options_tab, text="Options", bg="#B6C5CF", font=("Roboto", 12, "bold"))
options_label.pack(padx = 5, pady=5, side='top', anchor='w')

# CSV frame
csv_frame = tk.Frame(upper_frame, bg="#B6C5CF")
csv_frame.pack(side=tk.TOP, fill='x', padx=10, pady=(0, 5))

# CSV chooser
tk.Label(csv_frame, text="Choose CSV-file:").pack(pady=5)
entry_csv = tk.Entry(csv_frame, width=50)
entry_csv.pack()
tk.Button(csv_frame, text="Choose...", command=select_csv).pack(pady=2)

# Input images folder chooser
tk.Label(csv_frame, text="Choose input images folder:").pack(pady=5)
entry_img = tk.Entry(csv_frame, width=50)
entry_img.pack()
tk.Button(csv_frame, text="Choose...", command=select_in_folder).pack(pady=2)

# Output images folder chooser
tk.Label(csv_frame, text="Choose output folder:").pack(pady=5)
entry_out = tk.Entry(csv_frame, width=50)
entry_out.pack()
tk.Button(csv_frame, text="Choose...", command=select_out_folder).pack(pady=2)

# Middle frame
mid_frame = tk.Frame(root, bg="#F0F0F0", height=300)
mid_frame.pack(side=tk.TOP, expand=False, fill='x')

# Mid-buttons grid
buttons_frame = tk.Frame(mid_frame, bg="#F0F0F0")
buttons_frame.pack(pady=10)

# Run-button
run_button = tk.Button(buttons_frame, text="Run renamer", bg="green", fg="white", font=("Roboto", 12, "bold"), command=start_process)

run_button.grid(row=0, column=0, padx=10, pady=10, sticky='w')

# Reset-button
reset_button = tk.Button(buttons_frame, text="Reset", bg="red", fg="white", font=("Roboto", 12, "bold"), command=reset_all)

reset_button.grid(row=0, column=1, padx=10, pady=10, sticky='w')

# Switch window buttons
switch_button_f = tk.Button(buttons_frame, text="Functions view", bg="#347083", fg="white", font=("Roboto", 12, "bold"), command=show_functions_window)
switch_button_f.grid(row=0, column=2, padx=10, pady=10, sticky='w')

switch_button_c = tk.Button(buttons_frame, text="CSV view", bg="#347083", fg="white", font=("Roboto", 12, "bold"), command=show_csv_window)
switch_button_c.grid(row=0, column=3, padx=10, pady=10, sticky='w')
switch_button_c.grid_remove()

# Apply function button
apply_button = tk.Button(buttons_frame, text="Apply functions", bg="#CAC839", fg="white", font=("Roboto", 12, "bold"), command=apply_all_functions)
apply_button.grid(row=0, column=4, padx=10, pady=10, sticky='w')

# Drop frame
drop_frame = tk.Label(mid_frame, text="Drag and drop CSV file or image folder here", bg="#B6C5CF", font=("Roboto", 12), width=40, height=4, border = 2, relief="groove")
drop_frame.pack(expand=False, fill='both')

drop_frame.drop_target_register(DND_FILES)
drop_frame.dnd_bind('<<Drop>>', drop)

# Table Frame
table_window = tk.Frame(root, bg="#ADBBC4")
table_window.pack(side=tk.BOTTOM, expand=True, fill='both')

# Drop-down headings
headings_frame = tk.Frame(table_window, height=30, bg="#B6C5CF")
headings_frame.pack(fill='x')

headings_frame.grid_columnconfigure(0, weight=0, minsize=120)
headings_frame.grid_columnconfigure(1, weight=1)
headings_frame.grid_columnconfigure(2, weight=0)
headings_frame.grid_columnconfigure(3, weight=1)

h1 = tk.Label(headings_frame, text="File number", bg="#B6C5CF", font=("Roboto", 10, "bold"))
h2 = ttk.Combobox(headings_frame, values=["Files from input folder"], font=("Roboto", 10, "bold"), width=30, state="disabled")
h2.current(0)
h3 = ttk.Combobox(headings_frame, values=["Sort by", "Name", "Last modified", "Created"], font=("Roboto", 10, "bold"), width=15, state="readonly")
h3.current(0)
h4 = ttk.Combobox(headings_frame, values=["New name (Choose column)"], font=("Roboto", 10, "bold"), width=30, state="readonly")
h4.current(0)

h1.grid(row=0, column=0, padx=(10, 25), pady=5, sticky='ew')
h2.grid(row=0, column=1, padx=10, pady=5, sticky='w')
h3.grid(row=0, column=1, padx=10, pady=5, sticky='e')
h4.grid(row=0, column=3, padx=(0, 20), pady=5, sticky='w')

h3.bind("<<ComboboxSelected>>", lambda event: sort_name_by(tree))
h4.bind("<<ComboboxSelected>>", update_table)

# Table
columns = ("index", "current_name", "new_name")
tree = ttk.Treeview(table_window, columns=columns, show='headings')

tree.column("index", width=120, anchor='center', stretch=False)
tree.column("current_name", width=200, anchor='center', stretch=True)
tree.column("new_name", width=200, anchor='center', stretch=True)
tree.heading("index", text="#")
tree.heading("current_name", text="Current name")
tree.heading("new_name", text="New name")

scrollbar = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side='left', fill='both', expand=True)
scrollbar.pack(side='right', fill='y')

root.config(menu=menubar)
root.mainloop()