import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

def get_video_duration(video_file):
    # Use ffprobe to get video duration
    ffprobe_cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_file
    ]
    result = subprocess.run(ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return float(result.stdout)

# Function to execute ffmpeg trimming command
def trim_video():
    input_file = input_file_var.get()
    output_file = output_file_var.get()
    start_trim = start_slider.get()
    end_trim = end_slider.get()
    output_format = format_var.get()
    video_duration = get_video_duration(input_file)

    if not input_file or not output_file:
        messagebox.showerror("Error", "Please select both input and output files.")
        return

    # Modify output file extension based on selected format
    if output_format == "GIF":
        output_file = os.path.splitext(output_file)[0] + ".gif"
        # Use ffmpeg to generate a GIF
        try:
            ffmpeg_cmd = [
                "ffmpeg",
                "-i", input_file,
                "-ss", str(start_trim),
                "-t", str(video_duration - end_trim),
                "-vf", "fps=15,scale=640:-1:flags=lanczos",  # Adjust fps and scale for GIF
                "-y", output_file
            ]
            subprocess.run(ffmpeg_cmd, check=True)
            messagebox.showinfo("Success", "GIF created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create GIF: {str(e)}")
    else:
        # For MP4
        try:
            # Construct the ffmpeg command
            ffmpeg_cmd = [
                "ffmpeg",
                "-i", input_file,
                "-ss", str(start_trim),
                "-t", str(video_duration - end_trim),
                "-y", output_file
            ]
            subprocess.run(ffmpeg_cmd, check=True)
            messagebox.showinfo("Success", "Video trimmed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to trim video: {str(e)}")

# Function to open file dialog for selecting input file
def select_input_file():
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if file_path:
        input_file_var.set(file_path)

# Function to open file dialog for selecting output file
def select_output_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4"), ("GIF files", "*.gif")])
    if file_path:
        output_file_var.set(file_path)

# Create the main window
root = tk.Tk()
root.title("FFmpeg Video Trimmer")

# Input File Dropdown
input_file_var = tk.StringVar()
input_label = tk.Label(root, text="Input Video:")
input_label.grid(row=0, column=0, padx=10, pady=10)
input_dropdown = tk.Entry(root, textvariable=input_file_var, width=50)
input_dropdown.grid(row=0, column=1, padx=10, pady=10)
input_button = tk.Button(root, text="Browse", command=select_input_file)
input_button.grid(row=0, column=2, padx=10, pady=10)

# Output File Dropdown
output_file_var = tk.StringVar()
output_label = tk.Label(root, text="Output Video:")
output_label.grid(row=1, column=0, padx=10, pady=10)
output_dropdown = tk.Entry(root, textvariable=output_file_var, width=50)
output_dropdown.grid(row=1, column=1, padx=10, pady=10)
output_button = tk.Button(root, text="Browse", command=select_output_file)
output_button.grid(row=1, column=2, padx=10, pady=10)

# Sliders for trimming start and end
start_slider_label = tk.Label(root, text="Trim Seconds from Start:")
start_slider_label.grid(row=2, column=0, padx=10, pady=10)
start_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=300)
start_slider.grid(row=2, column=1, padx=10, pady=10)

end_slider_label = tk.Label(root, text="Trim Seconds from End:")
end_slider_label.grid(row=3, column=0, padx=10, pady=10)
end_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=300)
end_slider.grid(row=3, column=1, padx=10, pady=10)

# Format Selection (MP4 or GIF)
format_var = tk.StringVar(value="MP4")
format_label = tk.Label(root, text="Output Format:")
format_label.grid(row=4, column=0, padx=10, pady=10)
format_dropdown = tk.OptionMenu(root, format_var, "MP4", "GIF")
format_dropdown.grid(row=4, column=1, padx=10, pady=10)

# Trim Button
trim_button = tk.Button(root, text="Trim Video", command=trim_video)
trim_button.grid(row=5, column=1, padx=10, pady=10)

# Run the main loop
root.mainloop()
