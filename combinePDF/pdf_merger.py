import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
from PyPDF2 import PdfReader, PdfWriter
from datetime import datetime

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")

        self.pdf_files = []
        self.result_path = ''

        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.control_frame = tk.Frame(self.main_frame)
        self.control_frame.pack(side=tk.TOP, fill=tk.X)

        self.add_button = tk.Button(self.control_frame, text="Add PDF", command=self.add_files)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(self.control_frame, text="Delete Selected", command=self.delete_files)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.clear_button = tk.Button(self.control_frame, text="Clear All", command=self.clear_input_files)
        self.clear_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.merge_button = tk.Button(self.control_frame, text="Merge PDFs", command=self.merge_pdfs)
        self.merge_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.progress = ttk.Progressbar(self.control_frame, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.progress.pack(side=tk.LEFT, padx=5, pady=5)

        self.progress_label = tk.Label(self.control_frame, text="0%")
        self.progress_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.file_list_frame = tk.Frame(self.main_frame)
        self.file_list_frame.pack(fill=tk.BOTH, expand=True)

        self.file_listbox = tk.Listbox(self.file_list_frame, selectmode=tk.EXTENDED, cursor="hand2")
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.file_list_frame, orient=tk.VERTICAL)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.file_listbox.yview)

        self.arrow_frame = tk.Frame(self.file_list_frame)
        self.arrow_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.up_button = tk.Button(self.arrow_frame, text="↑", command=self.move_up)
        self.up_button.pack(side=tk.TOP, padx=5, pady=5)

        self.down_button = tk.Button(self.arrow_frame, text="↓", command=self.move_down)
        self.down_button.pack(side=tk.TOP, padx=5, pady=5)

        self.output_frame = tk.Frame(self.main_frame)
        self.output_frame.pack(fill=tk.X, pady=10)

        self.output_label = tk.Label(self.output_frame, text="Output Path: None", fg="blue", cursor="hand2")
        self.output_label.pack(side=tk.LEFT)
        self.output_label.bind("<Button-1>", self.open_output_file)

        # Log frame
        self.log_frame = tk.Frame(self.main_frame)
        self.log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.log_text = tk.Text(self.log_frame, height=10, state=tk.DISABLED)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.log_scrollbar = tk.Scrollbar(self.log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_text.config(yscrollcommand=self.log_scrollbar.set)

        # Error tag configuration
        self.log_text.tag_config("error", foreground="red")

        # Bind double-click event to open the selected file
        self.file_listbox.bind("<Double-1>", self.open_selected_file)

    def log(self, message, error=False):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        self.log_text.config(state=tk.NORMAL)
        if error:
            self.log_text.insert(tk.END, full_message + "\n", "error")
        else:
            self.log_text.insert(tk.END, full_message + "\n")
        self.log_text.config(state=tk.DISABLED)
        self.log_text.yview(tk.END)  # Automatically scroll to the end to show the newest log

    def add_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        if file_paths:
            # Clear the merged file information if new files are added
            self.clear_merged_file_info()

        for file_path in file_paths:
            if file_path not in self.pdf_files:
                self.pdf_files.append(file_path)
                self.file_listbox.insert(tk.END, file_path)
                self.log(f"Added file: {file_path}")

    def delete_files(self):
        selected_indices = list(self.file_listbox.curselection())
        if not selected_indices:
            messagebox.showerror("Error", "No PDF files selected")
            return

        for index in selected_indices[::-1]:
            self.log(f"Deleted file: {self.pdf_files[index]}")
            self.file_listbox.delete(index)
            del self.pdf_files[index]

    def move_up(self):
        selected_indices = list(self.file_listbox.curselection())
        if not selected_indices:
            return

        for index in selected_indices:
            if index == 0:
                continue
            file = self.pdf_files.pop(index)
            self.pdf_files.insert(index - 1, file)
            self.file_listbox.delete(index)
            self.file_listbox.insert(index - 1, file)

        # Re-select moved items
        for index in selected_indices:
            self.file_listbox.selection_set(index - 1)

        moved_files = [self.file_listbox.get(i - 1) for i in selected_indices]
        self.log(f"Moved up files: {', '.join(moved_files)}")

    def move_down(self):
        selected_indices = list(self.file_listbox.curselection())
        if not selected_indices:
            return

        selected_indices.reverse()
        for index in selected_indices:
            if index == len(self.pdf_files) - 1:
                continue
            file = self.pdf_files.pop(index)
            self.pdf_files.insert(index + 1, file)
            self.file_listbox.delete(index)
            self.file_listbox.insert(index + 1, file)

        # Re-select moved items
        for index in selected_indices:
            self.file_listbox.selection_set(index + 1)

        moved_files = [self.file_listbox.get(i + 1) for i in selected_indices]
        self.log(f"Moved down files: {', '.join(moved_files)}")

    def merge_pdfs(self):
        if not self.pdf_files:
            messagebox.showerror("Error", "No PDF files selected")
            self.log("No PDF files selected", error=True)
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", initialfile="merge.pdf",
                                                   filetypes=[("PDF files", "*.pdf")])
        if not output_path:
            return

        pdf_writer = PdfWriter()
        total_pages = 0

        # Calculate total number of pages
        valid_pdfs = []
        for path in self.pdf_files:
            try:
                pdf_reader = PdfReader(path)
                total_pages += len(pdf_reader.pages)
                valid_pdfs.append(path)
                self.log(f"Valid PDF: {path} with {len(pdf_reader.pages)} pages")
            except Exception as e:
                #messagebox.showerror("Error", f"An error occurred while reading '{path}': {e}")
                self.log(f"ignore file as Error reading '{path}': {e}", error=True)

        if not valid_pdfs:
            messagebox.showerror("Error", "No valid PDF files to merge")
            self.log("No valid PDF files to merge", error=True)
            return

        self.progress["maximum"] = total_pages
        current_page = 0

        try:
            for path in valid_pdfs:
                pdf_reader = PdfReader(path)
                for page in range(len(pdf_reader.pages)):
                    pdf_writer.add_page(pdf_reader.pages[page])
                    current_page += 1
                    self.progress["value"] = current_page
                    self.progress_label.config(text=f"{int((current_page / total_pages) * 100)}%")
                    self.root.update_idletasks()
                    self.log(f"Added page {page + 1} from {path}")

            with open(output_path, 'wb') as out:
                pdf_writer.write(out)

            messagebox.showinfo("Success", f"PDFs merged successfully into {output_path}")
            self.result_path = output_path
            self.output_label.config(text=f"Output Path: {output_path}")
            self.log(f"PDFs merged successfully into {output_path}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while merging PDFs: {e}")
            self.log(f"Error during merging: {e}", error=True)

        # self.progress["value"] = 0
        # self.progress_label.config(text="100%")

    def open_output_file(self, event):
        if self.result_path and os.path.exists(self.result_path):
            os.startfile(self.result_path)
        else:
            messagebox.showerror("Error", "No result file available")
            self.log("No result file available", error=True)

    def open_selected_file(self, event):
        selected_indices = self.file_listbox.curselection()
        if selected_indices:
            file_path = self.file_listbox.get(selected_indices[0])
            if os.path.exists(file_path):
                os.startfile(file_path)
            else:
                messagebox.showerror("Error", "Selected file does not exist")
                self.log(f"Selected file does not exist: {file_path}", error=True)

    def clear_merged_file_info(self):
        self.result_path = ''
        self.output_label.config(text="Output Path: None")
        self.progress["value"] = 0
        self.progress_label.config(text="0%")

    def clear_input_files(self):
        self.file_listbox.delete(0, tk.END)
        self.pdf_files.clear()
        self.clear_log()
        self.log("Cleared input files and log")
        self.progress["value"] = 0
        self.progress_label.config(text="0%")

    def clear_log(self):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.log("Log cleared")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
