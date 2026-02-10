import os
import pandas as pd
from natsort import natsorted
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import ttk

""" def load_asset(path):
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    assets = os.path.join(base, "assets")
    return os.path.join(assets, path)

canvas.place(x=0, y=0)

canvas.create_text(
    14,
    387,
    anchor="nw",
    text="",
    fill="#000000",
    font=("Default Font", 12 * -1)
)

button_1_image = tk.PhotoImage(file=load_asset("1.png"))

button_1 = tk.Button(
    image=button_1_image,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 has been pressed!")
)

button_1.place(x=14, y=356, width=80, height=30)

button_2_image = tk.PhotoImage(file=load_asset("2.png"))

button_2 = tk.Button(
    image=button_2_image,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 has been pressed!")
)

button_2.place(x=104, y=356, width=90, height=30)

button_3_image = tk.PhotoImage(file=load_asset("3.png"))

button_3 = tk.Button(
    image=button_3_image,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_3 has been pressed!")
)

button_3.place(x=204, y=356, width=80, height=30)

textbox_1 = tk.Entry(
    bd=0,
    bg="#000000",
    fg="#ffffff",
    insertbackground="#ffffff",
    highlightthickness=0
)

textbox_1.place(x=512, y=30, width=498, height=325)

textbox_2 = tk.Entry(
    bd=0,
    bg="#000000",
    fg="#ffffff",
    insertbackground="#ffffff",
    highlightthickness=0
)

textbox_2.place(x=14, y=30, width=498, height=325)

button_4_image = tk.PhotoImage(file=load_asset("4.png"))

button_4 = tk.Button(
    image=button_4_image,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 has been pressed!")
)

button_4.place(x=14, y=0, width=80, height=30)

button_5_image = tk.PhotoImage(file=load_asset("5.png"))

button_5 = tk.Button(
    image=button_5_image,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 has been pressed!")
)

button_5.place(x=104, y=0, width=80, height=30)

button_6_image = tk.PhotoImage(file=load_asset("6.png"))

button_6 = tk.Button(
    image=button_6_image,
    relief="flat",
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 has been pressed!")
)

button_6.place(x=194, y=0, width=88, height=30)


window.resizable(False, False)
window.mainloop() """


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

# Create window
root = tk.Tk()
root.title("Photo renamer")
root.geometry("1024x640")


#Menubar
menubar = Menu(root)

#File button
file = Menu(menubar, tearoff=0)
menubar.add_cascade(label='File', menu = file)
file.add_command(label = 'Choose Input Folder', command=select_in_folder)
file.add_command(label = 'Choose Output Folder', command=select_out_folder)
file.add_command(label = 'Choose CSV', command=select_csv)




# CSV chooser
tk.Label(root, text="Choose CSV-file:").pack(pady=5)
entry_csv = tk.Entry(root, width=50)
entry_csv.pack()
tk.Button(root, text="Choose...", command=select_csv).pack(pady=2)

# Input images folder chooser
button_1 = tk.Button(root, text='Choose Input')

tk.Label(root, text="Choose input images folder:").pack(pady=5)
entry_img = tk.Entry(root, width=50)
entry_img.pack()
tk.Button(root, text="Choose...", command=select_csv).pack(pady=2)

# Output images folder chooser
tk.Label(root, text="Choose output folder:").pack(pady=5)
entry_out = tk.Entry(root, width=50)
entry_out.pack()
tk.Button(root, text="Choose...", command=select_csv).pack(pady=2)

# Run-button
tk.Button(root, text="Run renamer", bg="green", fg="white", font=("Roboto", 12, "bold"), command=start_process).pack(pady=20)

# Table-window
table_window = tk.Frame(root, bg="#ADBBC4")
table_window.pack(expand=True, fill='both')

style = ttk.Style()
style.configure("Treeview", background="#ADBBC4", foreground="black", rowheight=25, fieldbackground="#ADBBC4")
style.map('Treeview', background=[('selected', '#347083')])

columns = ("index", "current_name", "new_name")
tree = ttk.Treeview(table_window, columns=columns, show='headings')

tree.heading("index", text="File #")
tree.heading("current_name", text="Current Name")
tree.heading("new_name", text="New Name")

tree.column("index", width=20, anchor='center')
tree.column("current_name", width=200, anchor='center')
tree.column("new_name", width=200, anchor='center')

scrollbar = ttk.Scrollbar(table_window, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side='left', fill='both', expand=True)
scrollbar.pack(side='right', fill='y')

root.config(menu=menubar)
root.mainloop()