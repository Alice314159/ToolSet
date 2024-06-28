import tkinter as tk
from tkinter import filedialog, scrolledtext, Menu
from PIL import Image, ImageTk
import pyautogui
import numpy as np
import cv2
import pytesseract
import pyperclip
from io import BytesIO
import win32clipboard
import os
import sys
from loguru import logger

# Setup logging
logger.add("capture.log")

if getattr(sys, 'frozen', False):
    # The application is frozen
    application_path = sys._MEIPASS
else:
    # The application is not frozen
    application_path = os.path.dirname(__file__)

tesseract_path = os.path.join(application_path, 'Tesseract-OCR', 'tesseract.exe')
logger.debug(f"Tesseract path set to: {tesseract_path}")
pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Specify the path to the Tesseract executable if it's not in your PATH
#pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'  # Update this path if necessary


class ScreenCaptureApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Capture Tool")
        self.root.iconbitmap('F:\\PackFolder\\cycling2Moon32.ico')
        # Bind the close event to the on_closing method
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Initialize coordinates and modes
        self.start_x = self.start_y = self.end_x = self.end_y = 0
        self.current_image = None
        self.mosaic_start_x = self.mosaic_start_y = self.mosaic_end_x = self.mosaic_end_y = 0
        self.is_mosaic_mode = False

        logger.debug("Application initialized, starting capture process.")
        # Start capturing immediately
        self.root.after(100, self.start_capture)

    def start_capture(self):
        logger.debug("Starting capture process.")
        if hasattr(self, 'image_window') and self.image_window.winfo_exists():
            self.image_window.withdraw()  # Hide the image window if it exists
        self.root.withdraw()  # Hide the main window
        self.capture_area()

    def capture_area(self):
        logger.debug("Capturing screen area.")
        self.capture_window = tk.Toplevel(self.root)
        self.capture_window.attributes("-fullscreen", True)
        self.capture_window.attributes("-alpha", 0.3)
        self.capture_window.bind("<Button-1>", self.on_button_press_capture)
        self.capture_window.bind("<B1-Motion>", self.on_mouse_drag_capture)
        self.capture_window.bind("<ButtonRelease-1>", self.on_button_release_capture)
        self.capture_canvas = tk.Canvas(self.capture_window, cursor="cross")
        self.capture_canvas.pack(fill=tk.BOTH, expand=tk.YES)

    def on_button_press_capture(self, event):
        logger.debug(f"Mouse pressed at ({event.x}, {event.y})")
        self.start_x = event.x
        self.start_y = event.y
        self.capture_canvas.delete("selection_rectangle")

    def on_mouse_drag_capture(self, event):
        self.capture_canvas.delete("selection_rectangle")
        self.capture_canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="red", fill="red",
                                             tag="selection_rectangle")


    def on_button_release_capture(self, event):

        self.end_x = event.x
        self.end_y = event.y
        self.capture_window.destroy()
        self.process_capture()
        self.show_image_window()

    def process_capture(self):
        x1 = min(self.start_x, self.end_x)
        y1 = min(self.start_y, self.end_y)
        x2 = max(self.start_x, self.end_x)
        y2 = max(self.start_y, self.end_y)

        logger.debug(f"Processing capture from ({x1}, {y1}) to ({x2}, {y2})")
        screenshot = pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))

        if screenshot is None:
            logger.error("Failed to capture screenshot.")
            return

        self.current_image = screenshot

    def show_image_window(self):
        logger.debug("Showing image window.")
        if hasattr(self, 'image_window') and self.image_window.winfo_exists():
            self.image_window.deiconify()
        else:
            self.image_window = tk.Toplevel(self.root)
            self.image_window.title("Image and Tools")
            self.image_window.iconbitmap('F:\\PackFolder\\cycling2Moon32.ico')  # Set the window icon
            # Bind the close event to the on_closing method
            self.image_window.protocol("WM_DELETE_WINDOW", self.on_closing)

            self.frame = tk.Frame(self.image_window)
            self.frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            self.recapture_button = tk.Button(self.frame, text="Recapture", command=self.start_capture)
            self.recapture_button.grid(row=0, column=0, padx=5)

            self.recognize_button = tk.Button(self.frame, text="Recognize", command=self.recognize_text)
            self.recognize_button.grid(row=0, column=1, padx=5)

            self.save_button = tk.Button(self.frame, text="Save", command=self.save_image)
            self.save_button.grid(row=0, column=2, padx=5)

            self.mosaic_button = tk.Button(self.frame, text="Mosaic", command=self.enable_mosaic_mode)
            self.mosaic_button.grid(row=0, column=3, padx=5)

            self.copy_button = tk.Button(self.frame, text="Copy", command=self.copy_image)
            self.copy_button.grid(row=0, column=4, padx=5)

            self.canvas_frame = tk.Frame(self.image_window)
            self.canvas_frame.grid(row=1, column=0, sticky="nsew")

            self.canvas = tk.Canvas(self.canvas_frame)
            self.canvas.grid(row=0, column=0, sticky="nsew")
            self.canvas.bind("<ButtonPress-1>", self.on_button_press)
            self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
            self.canvas.bind("<ButtonRelease-1>", self.on_button_release_mosaic)

            self.menu = Menu(self.image_window, tearoff=0)
            self.menu.add_command(label="Copy Text", command=self.copy_text)
            self.canvas.bind("<Button-3>", self.show_context_menu)

        self.update_image_window_size()
        self.display_image(self.current_image)

    def update_image_window_size(self):
        img_width, img_height = self.current_image.size
        self.image_window.geometry(f"{img_width + 400}x{img_height + 100}")
        self.image_window.minsize(img_width + 400, img_height + 100)
        self.image_window.maxsize(img_width + 800, img_height + 400)
        self.canvas.config(width=img_width, height=img_height)
        logger.debug(f"Updated image window size to ({img_width}, {img_height})")

    def display_image(self, image):
        self.image_tk = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        logger.debug("Displayed image on canvas.")

    def enhance_image(self, image):
        logger.debug("Enhancing image for OCR.")
        image_np = np.array(image)
        if image_np.size == 0:
            logger.error("Image conversion to NumPy array failed or image is empty.")
            return None

        image_gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        _, image_thresh = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        scale_percent = 200
        width = int(image_thresh.shape[1] * scale_percent / 100)
        height = int(image_thresh.shape[0] * scale_percent / 100)
        dim = (width, height)
        image_scaled = cv2.resize(image_thresh, dim, interpolation=cv2.INTER_LINEAR)

        return image_scaled

    def recognize_text(self):
        logger.debug("Recognizing text from image.")
        if self.current_image is None:
            logger.error("No image to perform OCR on.")
            return

        screenshot_enhanced = self.enhance_image(self.current_image)
        if screenshot_enhanced is None:
            logger.error("screenshot_enhanced is None.")
            return

        text = self.run_ocr(screenshot_enhanced)
        self.update_text_display(text)

    def run_ocr(self, image):
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        logger.debug(f"Recognized text: {text}")
        return text

    def update_text_display(self, text):
        img_width, img_height = self.current_image.size
        self.image_window.geometry(f"{img_width + 400}x{img_height + 100}")
        self.text_display = scrolledtext.ScrolledText(self.image_window, width=50, height=img_height // 12, wrap=tk.WORD)
        self.text_display.grid(row=1, column=1, padx=10, pady=10, sticky="ns")
        self.text_display.delete(1.0, tk.END)
        self.text_display.insert(tk.END, text)
        self.text_display.bind("<Button-3>", self.show_text_context_menu)
        logger.debug("Updated text display.")

    def show_context_menu(self, event):
        self.menu.tk_popup(event.x_root, event.y_root)

    def show_text_context_menu(self, event):
        text_menu = Menu(self.text_display, tearoff=0)
        text_menu.add_command(label="Copy", command=self.copy_selected_text)
        text_menu.tk_popup(event.x_root, event.y_root)

    def copy_selected_text(self):
        selected_text = self.text_display.get(tk.SEL_FIRST, tk.SEL_LAST)
        pyperclip.copy(selected_text)
        logger.debug("Copied selected text to clipboard.")

    def copy_text(self):
        selected_text = self.text_display.get("1.0", tk.END)
        pyperclip.copy(selected_text)
        logger.debug("Copied all text to clipboard.")

    def save_image(self):
        logger.debug("Saving image.")
        if self.current_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if save_path:
                self.current_image.save(save_path)
                logger.debug(f"Image saved to {save_path}")

    def enable_mosaic_mode(self):
        self.is_mosaic_mode = True
        logger.debug("Mosaic mode enabled.")

    def on_button_press(self, event):
        if self.is_mosaic_mode:
            self.mosaic_start_x = self.canvas.canvasx(event.x)
            self.mosaic_start_y = self.canvas.canvasy(event.y)
            logger.debug(f"Mosaic start position: ({self.mosaic_start_x}, {self.mosaic_start_y})")
        else:
            self.canvas.scan_mark(event.x, event.y)
            logger.debug(f"Canvas scan mark position: ({event.x}, {event.y})")

    def on_mouse_drag(self, event):
        if self.is_mosaic_mode:
            self.canvas.delete("mosaic_rectangle")
            self.canvas.create_rectangle(self.mosaic_start_x, self.mosaic_start_y, self.canvas.canvasx(event.x),
                                         self.canvas.canvasy(event.y), outline="blue", tag="mosaic_rectangle")
            logger.debug(f"Mosaic drag position: ({self.canvas.canvasx(event.x)}, {self.canvas.canvasy(event.y)})")
        else:
            self.canvas.scan_dragto(event.x, event.y, gain=1)
            logger.debug(f"Canvas scan drag position: ({event.x}, {event.y})")

    def on_button_release_mosaic(self, event):
        if self.is_mosaic_mode:
            self.mosaic_end_x = self.canvas.canvasx(event.x)
            self.mosaic_end_y = self.canvas.canvasy(event.y)
            logger.debug(f"Mosaic end position: ({self.mosaic_end_x}, {self.mosaic_end_y})")
            self.apply_mosaic()
            self.is_mosaic_mode = False

    def apply_mosaic(self):
        logger.debug("Applying mosaic.")
        if self.current_image is None:
            logger.error("No image to apply mosaic on.")
            return

        x1 = int(min(self.mosaic_start_x, self.mosaic_end_x))
        y1 = int(min(self.mosaic_start_y, self.mosaic_end_y))
        x2 = int(max(self.mosaic_start_x, self.mosaic_end_x))
        y2 = int(max(self.mosaic_start_y, self.mosaic_end_y))

        image_np = np.array(self.current_image)
        mosaic_area = image_np[y1:y2, x1:x2]
        mosaic_area = cv2.resize(mosaic_area, (10, 10), interpolation=cv2.INTER_LINEAR)
        mosaic_area = cv2.resize(mosaic_area, (x2 - x1, y2 - y1), interpolation=cv2.INTER_NEAREST)
        image_np[y1:y2, x1:x2] = mosaic_area

        self.current_image = Image.fromarray(image_np)
        self.display_image(self.current_image)
        logger.debug("Mosaic applied.")

    def copy_image(self):
        if self.current_image:
            logger.debug("Copying image to clipboard.")
            output = BytesIO()
            self.current_image.convert("RGB").save(output, "BMP")
            data = output.getvalue()[14:]
            output.close()

            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
            win32clipboard.CloseClipboard()
            logger.debug("Image copied to clipboard.")
        else:
            logger.error("Copying image error.")

    def on_closing(self):
        logger.debug("Application exiting.")
        self.root.quit()
        self.root.destroy()
        sys.exit()


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenCaptureApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)  # Handle close button
    root.mainloop()
