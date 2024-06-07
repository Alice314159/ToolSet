import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
import pillow_heif

# Add support for HEIF format
pillow_heif.register_heif_opener()


class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Converter")

        self.frame = tk.Frame(root)
        self.frame.pack(pady=20)

        self.add_button = tk.Button(self.frame, text="Add Images", command=self.add_images)
        self.add_button.grid(row=0, column=0, padx=10)

        self.delete_button = tk.Button(self.frame, text="Delete Selected", command=self.delete_selected)
        self.delete_button.grid(row=0, column=1, padx=10)

        self.convert_button = tk.Button(self.frame, text="Convert to JPG", command=self.convert_to_jpg)
        self.convert_button.grid(row=0, column=2, padx=10)

        self.check_button = tk.Button(self.frame, text="Check Result", command=self.check_result)
        self.check_button.grid(row=0, column=3, padx=10)

        self.image_paths = []
        self.converted_paths = []
        self.output_directory = ""

        # Frame to show selected image paths
        self.selected_frame = tk.LabelFrame(root, text="Selected Images", padx=10, pady=10)
        self.selected_frame.pack(pady=10, fill="both", expand="yes")

        self.selected_listbox = tk.Listbox(self.selected_frame, width=80, height=10, selectmode=tk.MULTIPLE)
        self.selected_listbox.pack(side="left", fill="both", expand="yes")
        self.selected_listbox.bind("<Double-1>", self.open_file)

        self.selected_scrollbar = tk.Scrollbar(self.selected_frame, orient="vertical")
        self.selected_scrollbar.pack(side="right", fill="y")

        self.selected_listbox.config(yscrollcommand=self.selected_scrollbar.set)
        self.selected_scrollbar.config(command=self.selected_listbox.yview)

        # Frame to show converted image paths
        self.converted_frame = tk.LabelFrame(root, text="Converted Images", padx=10, pady=10)
        self.converted_frame.pack(pady=10, fill="both", expand="yes")

        self.converted_listbox = tk.Listbox(self.converted_frame, width=80, height=10)
        self.converted_listbox.pack(side="left", fill="both", expand="yes")
        self.converted_listbox.bind("<Double-1>", self.open_file)

        self.converted_scrollbar = tk.Scrollbar(self.converted_frame, orient="vertical")
        self.converted_scrollbar.pack(side="right", fill="y")

        self.converted_listbox.config(yscrollcommand=self.converted_scrollbar.set)
        self.converted_scrollbar.config(command=self.converted_listbox.yview)

    def add_images(self):
        new_paths = filedialog.askopenfilenames(title="Add Images",
                                                filetypes=(("Image files", "*.png *.heic *.jpeg *.jpg *.webp"),
                                                           ("All files", "*.*")))
        if new_paths:
            self.converted_paths = []
            self.converted_listbox.delete(0, tk.END)
            self.image_paths = []
            self.selected_listbox.delete(0, tk.END)
            for path in new_paths:
                self.image_paths.append(path)
                self.selected_listbox.insert(tk.END, path)
            messagebox.showinfo("Images Added", f"Added {len(new_paths)} images.")

    def delete_selected(self):
        selected_indices = list(self.selected_listbox.curselection())
        if not selected_indices:
            messagebox.showwarning("No Selection", "Please select images to delete.")
            return

        for index in reversed(selected_indices):
            self.selected_listbox.delete(index)
            del self.image_paths[index]

        messagebox.showinfo("Images Deleted", f"Deleted {len(selected_indices)} images.")

    def convert_to_jpg(self):
        if not self.image_paths:
            messagebox.showwarning("No Images", "Please add images first.")
            return

        default_output_directory = os.path.dirname(self.image_paths[-1])
        self.output_directory = filedialog.askdirectory(initialdir=default_output_directory,
                                                        title="Select Output Directory")

        if not self.output_directory:
            messagebox.showwarning("No Output Directory", "Please set the output directory.")
            return

        self.converted_paths = []
        self.converted_listbox.delete(0, tk.END)

        for img_path in self.image_paths:
            img = Image.open(img_path)
            jpg_path = os.path.join(self.output_directory, os.path.basename(img_path).rsplit('.', 1)[0] + ".jpg")
            img.convert('RGB').save(jpg_path, "JPEG")
            self.converted_paths.append(jpg_path)
            self.converted_listbox.insert(tk.END, jpg_path)

        messagebox.showinfo("Conversion Complete", f"Converted {len(self.converted_paths)} images to JPG format.")

    def check_result(self):
        if not self.converted_paths:
            messagebox.showwarning("No Converted Images", "Please convert images first.")
            return

        if os.path.exists(self.output_directory):
            os.startfile(self.output_directory)
        else:
            messagebox.showerror("Error", "Output directory does not exist.")

    def open_file(self, event):
        widget = event.widget
        index = widget.curselection()
        if index:
            file_path = widget.get(index[0])
            os.startfile(file_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
