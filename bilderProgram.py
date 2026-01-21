import os
import pandas as pd
from natsort import natsorted
import tkinter as tk
from tkinter import filedialog, messagebox


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
    path = filedialog.askdirectory
    entry_img.delete(0, tk.END)
    entry_img.insert(0, path)

def select_out_folder():
    path = filedialog.askdirectory
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
root.geometry("350x500")

# CSV chooser
tk.Label(root, text="Choose CSV-file:").pack(pady=5)
entry_csv = tk.Entry(root, width=50)
entry_csv.pack()
tk.Button(root, text="Choose...", command=select_csv).pack(pady=2)

# Input images folder chooser
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

root.mainloop()