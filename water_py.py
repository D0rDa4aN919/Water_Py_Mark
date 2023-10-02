from platform import system
import tkinter as tk
from tkinter import filedialog

from PIL import Image, ImageTk


class WaterMark:
    def __init__(self, logo, image):
        self.copy, self.logo_size, self.image_size, self.logo_size, \
            self.position, self.directory_file = None, None, None, None, None, None
        self.logo = Image.open(logo)
        self.image = Image.open(image)
        self.full_name = image.split('/')[-1]
        self.file_name = self.full_name.split('.')[0]
        self.extension = self.full_name.split('.')[-1]
        self.counter = 0
        self.calculate_sizes()
        self.calculate_position()

    def calculate_sizes(self):
        width, height = self.image.size
        self.image_size = (int(width / 2), int(height / 2))
        self.image = self.image.resize(self.image_size)
        width, height = self.logo.size
        self.logo_size = (int(width / 4), int(height / 4))
        self.logo = self.logo.resize(self.logo_size)

    def calculate_position(self):
        image_width, image_height = self.image.size
        logo_width, logo_height = self.logo.size
        # Check if the logo fits inside the image
        if logo_width < image_width and logo_height < image_height:
            # Calculate the position to put the logo in the bottom-right corner
            self.position = (image_width - logo_width, image_height - logo_height)
        else:
            # If the logo is larger than the image, place it in the top-left corner
            self.position = (0, 0)

    def set_images(self, directory):
        self.directory_file = f"{directory}/{self.file_name}_mark{self.counter}.{self.extension}"
        self.copy = self.image.copy()
        self.copy.paste(self.logo, self.position)
        self.copy.save(self.directory_file)
        self.counter += 1


class Display(tk.Tk):
    def __init__(self):
        super().__init__()
        self.image_label, self.image, self.image_browser, \
            self.logo_title, self.logo_image, self.icon_browser, \
            self.main_button, self.directory = None, None, None, None, None, None, None, None
        self.title('Image  Watermark')
        self.geometry('1000x300')
        self.configure(background="#CBFF6A")
        # the main title
        self.title_window = tk.Label(self, text="Image Watermark", font=("Arial", 30, "bold"), bg="#CBFF6A")
        self.title_window.grid(row=0, column=1, sticky="nsew")
        self.grid_columnconfigure(self.title_window, weight=1)
        self.create_main_directory()
        self.make_display()

    def create_main_directory(self):
        import getpass
        user = getpass.getuser().strip(' ')
        if system() == "Windows":
            import os
            self.directory = f"C:\\Users\\{user}\\images"
            os.makedirs(self.directory, exist_ok=True)
        else:
            import subprocess
            self.directory = f"/home/{user}/images"
            subprocess.run(["mkdir", "-p", self.directory])

    def make_display(self):
        # the text of the entering image

        self.image_label = tk.Label(self, text="Enter image to insert to: ", font=("Arial", 20, "bold"), bg="#CBFF6A")
        self.image_label.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        # the text input of the entering image
        self.image = tk.Entry(self, bg="#CBFF6A", width=50, background="white", highlightthickness=2)
        self.image.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        # file explorer image browser button
        self.image_browser = tk.Button(self, text="Browser", width=10, highlightthickness=2,
                                       command=lambda x=self.image: self.browser(x))
        self.image_browser.grid(row=1, column=2, sticky="nsew", padx=10, pady=10)
        # the text of the entering logo
        self.logo_title = tk.Label(self, text="Enter image to insert to: ", font=("Arial", 20, "bold"), bg="#CBFF6A")
        self.logo_title.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        # the text input of the entering logo
        self.logo_image = tk.Entry(self, bg="#CBFF6A", width=50, background="white", highlightthickness=2)
        self.logo_image.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
        # file explorer icon browser button
        self.icon_browser = tk.Button(self, text="Browser", width=10, highlightthickness=2,
                                      command=lambda x=self.logo_image: self.browser(x))
        self.icon_browser.grid(row=2, column=2, sticky="nsew", padx=10, pady=10)
        self.main_button = tk.Button(self, text="Watermark", width=10, highlightthickness=2,
                                     font=("Arial", 24, "bold"), command=self.set_image)
        self.main_button.grid(row=3, column=1, padx=10, pady=10)
        # configure the grid
        self.grid_columnconfigure(0, weight=0)

    @staticmethod
    def browser(inputer):
        inputer.delete(0, tk.END)
        filename = filedialog.askopenfilename(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("jpg files", "*.jpg*"),
                                                         ("all files", "*.*")))
        # Change label contents
        inputer.insert(0, filename)

    def set_image(self):
        mark = WaterMark(self.logo_image.get(), self.image.get())
        mark.set_images(self.directory)
        # Open a new window to display the watermarked image
        result_window = ResultDisplay(mark)
        result_window.mainloop()


class ResultDisplay(tk.Toplevel):
    def __init__(self, mark):
        super().__init__()
        self.title('Watermarked Image')
        self.geometry('600x600')  # Set the initial size of the window
        self.configure(background="#CBFF6A")
        image_path = mark.directory_file
        self.watermarked_image = Image.open(image_path)

        # Get the size of the Tkinter window
        window_width = self.winfo_reqwidth()
        window_height = self.winfo_reqheight()

        # Resize the image to fit the Tkinter window
        resized_image = self.watermarked_image.resize((window_width, window_height))

        self.display_image = ImageTk.PhotoImage(resized_image)

        # Display the image on a label
        self.image_label = tk.Label(self, image=self.display_image)
        self.image_label.pack(expand="true")

        # Button to close the window
        self.close_button = tk.Button(self, text="Close", command=self.destroy)
        self.close_button.pack()


def main():
    window = Display()
    window.mainloop()


if __name__ == "__main__":
    main()
