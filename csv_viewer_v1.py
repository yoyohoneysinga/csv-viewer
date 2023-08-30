import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd

def load_csv_data():
    file_path = entry_file_path.get()

    try:
        data = pd.read_csv(file_path)
        display_data(data)
        result_label.config(text="")
    except FileNotFoundError:
        result_label.config(text="File not found.")
        tree.delete(*tree.get_children())
    except pd.errors.EmptyDataError:
        result_label.config(text="Empty CSV file.")
        tree.delete(*tree.get_children())
    except Exception as e:
        result_label.config(text=f"Error: {e}")
        tree.delete(*tree.get_children())

def display_data(data):
    headings = data.columns.tolist()
    tree.delete(*tree.get_children())
    tree['columns'] = headings

    for heading in headings:
        tree.heading(heading, text=heading)

    # Calculate column widths based on content
    for i, heading in enumerate(headings):
        content_length = max(data[heading].astype(str).apply(len).max(), len(heading))
        tree.column(heading, width=content_length * 10)  # Adjust the factor for desired spacing

    for _, row in data.iterrows():
        values = [row[heading] for heading in headings]
        tree.insert("", "end", values=values)

    tree.column("0", width=0)  # Hide the first column

    for heading in headings:
        tree.column(heading, anchor='center', stretch=1)

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    entry_file_path.delete(0, "end")
    entry_file_path.insert(0, file_path)

root = tk.Tk()
root.title("CSV Viewer")

# Center the input and submit button
frame_input = tk.Frame(root)
frame_input.pack(padx=10, pady=10)
frame_input.columnconfigure(0, weight=1)

label_file_path = tk.Label(frame_input, text="Enter CSV file path:")
label_file_path.pack(side="left")

entry_file_path = tk.Entry(frame_input, width=40)
entry_file_path.pack(side="left", padx=5)

browse_button = tk.Button(frame_input, text="Browse", command=browse_file)
browse_button.pack(side="left", padx=5)

button_submit = tk.Button(frame_input, text="Submit", command=load_csv_data)
button_submit.pack(side="left", padx=5)

result_label = tk.Label(root, text="")
result_label.pack(padx=10, pady=5)

tree = ttk.Treeview(root)
tree.pack(fill="both", expand=True, padx=10, pady=10)
tree.column("#0", width=0)  # Hide the first column

root.mainloop()
