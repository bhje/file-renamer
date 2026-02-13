import os
import pandas as pd
import csv
from natsort import natsorted
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk
import tkinterdnd2
from tkinterdnd2 import DND_FILES, TkinterDnD

def run_renamer(csv_path, images_folder, output_folder):
    try:
        # Create output folder if one does not exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        csvfName = pd.read_csv(csv_path, usecols=[3, 4])

        count = 0

        for index, row in csvfName.iterrows():
            name = str(row[0]+row[1])
            nameNoSpace = name.replace(" ", "")

            dir_list = os.listdir(images_folder)
            sortedlist = natsorted(dir_list)

            target_filename = str(index) + ".jpg"
            

            if len(sortedlist) > 0:
                if sortedlist[0] == target_filename:
                    src = os.path.join(images_folder, sortedlist[0])
                    dst = os.path.join(output_folder, nameNoSpace + ".jpg")
                    os.rename(src, dst)
                    count += 1
                else:
                    print(f"Skipped index {index}: {sortedlist[0]} != {target_filename}")

        messagebox.showinfo("Done!", f"The process has completed. \n{count} photos were renamed.")

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: \n{str(e)}")

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
def load_table(data, tree, col_idx_curr = 0, col_idx_new = 1):
    for item in tree.get_children():
        tree.delete(item)

    if h2.get() == "Current name (Choose column)":
        col_idx_curr = 0
    if h3.get() == "New name (Choose column)":
        col_idx_new = 1

    for i, row in enumerate(data[1:], start = 1):
        try:
            file_num = str(i)

            if len(row) > max(col_idx_curr, col_idx_new):
                current_name = row[col_idx_curr]
                new_name = row[col_idx_new]
                tree.insert("", "end", values=(file_num, current_name, new_name))

        except IndexError:
            tree.insert("", "end", values=row)

# Load table from csv path
def csv_to_table(csv_path, tree):
    try:
        with open(csv_path, mode = 'r', encoding='utf-8', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)
    except FileNotFoundError:
        messagebox.showerror("Error", f"File not found: {csv_path}")
    
    load_table(data, tree)
    update_dropdowns(data)

    print("Table loaded with new data.")

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
        entry_img.delete(0, tk.END)
        entry_img.insert(0, file_path)
    else:
        messagebox.showerror("Error", "Please drop a CSV file or an image folder.")

# Column names to drop-downs
def update_dropdowns(data):
    columns = data[0]

    h2['values'] = columns
    h3['values'] = columns

# Update table when drop-down selection changes
def update_table(event):
    col_idx_curr = h2.current()
    col_idx_new = h3.current()

    if col_idx_curr >= 0 or col_idx_new >= 0:
        csv_path = entry_csv.get()
        if csv_path:
            try:
                with open(csv_path, mode = 'r', encoding='utf-8', newline='') as file:
                    reader = csv.reader(file)
                    data = list(reader)
                load_table(data, tree, col_idx_curr, col_idx_new)
            except FileNotFoundError:
                messagebox.showerror("Error", f"File not found: {csv_path}")
        else:
            messagebox.showwarning("Warning", "Please choose a CSV file first.")

# Create window
root = TkinterDnD.Tk()
root.title("File renamer")
root.geometry("1024x640")

# Paned window
paned_window = ttk.Panedwindow(root, orient=tk.VERTICAL)
paned_window.pack(fill=tk.BOTH, expand=True)

#Menubar
menubar = Menu(root)

#Menubar file button
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu = file)
file.add_command(label = 'Choose Input Folder', command=select_in_folder)
file.add_command(label = 'Choose Output Folder', command=select_out_folder)
file.add_command(label = 'Choose CSV', command=select_csv)

# Chooser Frame
chooser_frame = tk.Frame(paned_window, height=150, bg="#F0F0F0")
chooser_frame.pack(expand=False, fill='x')

paned_window.add(chooser_frame)

# CSV chooser
tk.Label(chooser_frame, text="Choose CSV-file:").pack(pady=5)
entry_csv = tk.Entry(chooser_frame, width=50)
entry_csv.pack()
tk.Button(chooser_frame, text="Choose...", command=select_csv).pack(pady=2)

# Input images folder chooser
tk.Label(chooser_frame, text="Choose input images folder:").pack(pady=5)
entry_img = tk.Entry(chooser_frame, width=50)
entry_img.pack()
tk.Button(chooser_frame, text="Choose...", command=select_in_folder).pack(pady=2)

# Output images folder chooser
tk.Label(chooser_frame, text="Choose output folder:").pack(pady=5)
entry_out = tk.Entry(chooser_frame, width=50)
entry_out.pack()
tk.Button(chooser_frame, text="Choose...", command=select_out_folder).pack(pady=2)

# Run-button
tk.Button(chooser_frame, text="Run renamer", bg="green", fg="white", font=("Roboto", 12, "bold"), command=start_process).pack(pady=20)

# Drop frame
drop_frame = tk.Label(chooser_frame, text="Drag and drop CSV file or image folder here", bg="#B6C5CF", font=("Roboto", 12), width=40, height=4, border = 2, relief="groove")
drop_frame.pack(expand=True, fill='both')

drop_frame.drop_target_register(DND_FILES)
drop_frame.dnd_bind('<<Drop>>', drop)

# Table Frame
table_window = tk.Frame(paned_window, bg="#ADBBC4")
table_window.pack(expand=True, fill='both')

paned_window.add(table_window)

# Drop-down headings
headings_frame = tk.Frame(table_window, height=30, bg="#B6C5CF")
headings_frame.pack(expand=False, fill='x')

h1 = tk.Label(headings_frame, text="File number", bg="#B6C5CF", font=("Roboto", 10, "bold"))
h2 = ttk.Combobox(headings_frame, values=["Current name (Choose column)"], font=("Roboto", 10, "bold"), width=30)
h2.current(0)
h3 = ttk.Combobox(headings_frame, values=["New name (Choose column)"], font=("Roboto", 10, "bold"), width=30)
h3.current(0)

h1.grid(row=0, column=0, padx=(10, 25), pady=5)
h2.grid(row=0, column=1, padx=(10, 210), pady=5)
h3.grid(row=0, column=2, pady=5)

h2.bind("<<ComboboxSelected>>", update_table)
h3.bind("<<ComboboxSelected>>", update_table)

# Table
style = ttk.Style()
style.configure("Treeview", background="#ADBBC4", foreground="black", rowheight=25, fieldbackground="#ADBBC4")
style.map('Treeview', background=[('selected', '#347083')])

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