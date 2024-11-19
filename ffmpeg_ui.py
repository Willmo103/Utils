"""
Module to convert an MP4 video to a GIF using a GUI interface.
The user can select an input MP4 video file, specify an output GIF file,
and adjust the trimming and quality settings for the GIF conversion.
The conversion process is handled by ffmpeg, which must be installed on the system.
"""
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess


def get_video_duration(video_file):
    """Retrieve the duration of a video file using ffprobe."""
    try:
        ffprobe_cmd = [
            "ffprobe",
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_file
        ]
        result = subprocess.run(
            ffprobe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return float(result.stdout.strip())
    except subprocess.CalledProcessError:
        messagebox.showerror(
            "Error", "Failed to get video duration. Ensure ffprobe is installed and the input file is valid.")
        return None


def trim_to_gif():
    """Convert the input MP4 video to a trimmed GIF."""
    input_file = input_file_var.get()
    output_file = output_file_var.get()
    start_trim = start_slider.get()
    end_trim = end_slider.get()
    quality = quality_slider.get()

    # Validate inputs
    if not input_file or not os.path.isfile(input_file):
        messagebox.showerror("Error", "Please select a valid input MP4 file.")
        return

    if not output_file:
        messagebox.showerror("Error", "Please specify an output file.")
        return

    video_duration = get_video_duration(input_file)
    if video_duration is None:
        return

    # Ensure trim values are within valid range
    if start_trim + end_trim >= video_duration:
        messagebox.showerror("Error", "Trim values exceed video duration.")
        return

    # Adjust output file extension to .gif
    output_file = os.path.splitext(output_file)[0] + ".gif"

    # Calculate quality settings
    fps = 10 + (quality * 5)  # Frame rate increases with quality
    scale = 240 + (quality * 80)  # Resolution increases with quality

    try:
        # Construct ffmpeg command for GIF conversion
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", input_file,
            "-ss", str(start_trim),
            "-t", str(video_duration - start_trim - end_trim),
            "-vf", f"fps={fps},scale={scale}:-1:flags=lanczos",
            "-y", output_file
        ]

        # Execute ffmpeg command
        subprocess.run(ffmpeg_cmd, check=True, stderr=subprocess.PIPE)
        messagebox.showinfo(
            "Success", f"GIF saved successfully: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to process video: {str(e)}")


def select_input_file():
    """Open file dialog to select the input MP4 video."""
    file_path = filedialog.askopenfilename(filetypes=[("MP4 files", "*.mp4")])
    if file_path:
        input_file_var.set(file_path)
        video_duration = get_video_duration(file_path)
        if video_duration:
            start_slider.config(to=video_duration)
            end_slider.config(to=video_duration)


def select_output_file():
    """Open file dialog to select the output GIF file."""
    file_path = filedialog.asksaveasfilename(
        defaultextension=".gif", filetypes=[("GIF files", "*.gif")])
    if file_path:
        output_file_var.set(file_path)


# Create the main window
root = tk.Tk()
root.title("MP4 to GIF Converter")
root.geometry("600x450")

# Input File Selection
input_file_var = tk.StringVar()
tk.Label(root, text="Input MP4 Video:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=input_file_var, width=50).grid(
    row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_input_file).grid(
    row=0, column=2, padx=10, pady=10)

# Output File Selection
output_file_var = tk.StringVar()
tk.Label(root, text="Output GIF File:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=output_file_var, width=50).grid(
    row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=select_output_file).grid(
    row=1, column=2, padx=10, pady=10)

# Trimming sliders
tk.Label(root, text="Trim Seconds from Start:").grid(
    row=2, column=0, padx=10, pady=10)
start_slider = tk.Scale(root, from_=0, to=100,
                        orient=tk.HORIZONTAL, length=300)
start_slider.grid(row=2, column=1, padx=10, pady=10)

tk.Label(root, text="Trim Seconds from End:").grid(
    row=3, column=0, padx=10, pady=10)
end_slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, length=300)
end_slider.grid(row=3, column=1, padx=10, pady=10)

# Quality slider
tk.Label(root, text="GIF Quality (1-5):").grid(row=4,
                                               column=0, padx=10, pady=10)
quality_slider = tk.Scale(
    root, from_=1, to=5, orient=tk.HORIZONTAL, length=300)
quality_slider.grid(row=4, column=1, padx=10, pady=10)

# Convert button
tk.Button(root, text="Convert to GIF", command=trim_to_gif).grid(
    row=5, column=1, pady=20)

# Run the application
root.mainloop()
