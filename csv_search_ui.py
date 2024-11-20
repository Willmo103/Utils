# File: view_csv_app.py
# Description: Tkinter app to search and display the Packsize CSV.
import tkinter as tk
from tkinter import filedialog, ttk
import csv


def load_csv(file_path, treeview):
    global all_data  # Store all data for filtering
    all_data = []

    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            headers = next(reader)

            # Set up the Treeview columns
            treeview["columns"] = headers
            treeview["show"] = "headings"  # Show only headers
            for header in headers:
                treeview.heading(header, text=header)
                treeview.column(header, anchor="center")

            # Clear existing rows
            for row in treeview.get_children():
                treeview.delete(row)

            # Insert rows from CSV
            for row in reader:
                all_data.append(row)
                treeview.insert("", "end", values=row)
    except Exception as e:
        print(f"Error loading CSV: {e}")


def filter_csv(treeview, query):
    # Clear existing rows
    for row in treeview.get_children():
        treeview.delete(row)

    # Filter data and re-insert rows
    filtered_data = [
        # Search by Item Number
        row for row in all_data if query.lower() in row[0].lower()]
    for row in filtered_data:
        treeview.insert("", "end", values=row)


def open_file(treeview):
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        load_csv(file_path, treeview)


def main():
    global all_data
    all_data = []  # Store all rows of data for filtering

    root = tk.Tk()
    root.title("Packsize CSV Viewer")

    # Search bar
    search_frame = tk.Frame(root)
    search_frame.pack(fill="x", padx=10, pady=5)

    search_label = tk.Label(search_frame, text="Search Item Number:")
    search_label.pack(side="left")

    search_entry = tk.Entry(search_frame)
    search_entry.pack(side="left", fill="x", expand=True, padx=5)

    search_button = tk.Button(
        search_frame, text="Search", command=lambda: filter_csv(treeview, search_entry.get()))
    search_button.pack(side="right")

    # Treeview for displaying CSV content
    treeview = ttk.Treeview(root)
    treeview.pack(expand=True, fill="both")

    # Add Scrollbars
    # vsb = ttk.Scrollbar(root, orient="vertical", command=treeview.yview)
    # vsb.pack(side="right", fill="y")
    # treeview.configure(yscrollcommand=vsb.set)

    # Button to open CSV
    open_button = tk.Button(root, text="Open CSV",
                            command=lambda: open_file(treeview))
    open_button.pack(side="bottom", pady=5)

    root.geometry("800x600")
    root.mainloop()


if __name__ == '__main__':
    main()
