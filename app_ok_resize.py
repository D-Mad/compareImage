from tkinter import *
from PIL import Image, ImageTk
from tkinter import filedialog

class ImageSlider(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.image1 = None
        self.image2 = None

        self.width = 0
        self.height = 0

        self.canvas = Canvas(self)
        self.canvas.pack()

        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)

        self.load_button = Button(self, text="Load Images", command=self.load_images)
        self.load_button.pack(side=TOP, padx=5, pady=5)

    def load_images(self):
        image_file1 = filedialog.askopenfilename(title="Select Image 1", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        image_file2 = filedialog.askopenfilename(title="Select Image 2", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if image_file1 and image_file2:
            self.image1 = Image.open(image_file1)
            self.image2 = Image.open(image_file2)
            img_width, img_height = self.image1.size

            # Resize the canvas to fit the image size if image size is smaller than canvas size
            if img_width <= self.winfo_screenwidth() and img_height <= self.winfo_screenheight():
                self.width, self.height = img_width, img_height
                self.canvas.config(width=self.width, height=self.height)
            else:
                # Resize the image to fit the canvas size if the image is larger than the canvas size
                scale = min(self.winfo_screenwidth()/img_width, self.winfo_screenheight()/img_height)
                self.width, self.height = int(img_width * scale), int(img_height * scale)
                self.image1 = self.image1.resize((self.width, self.height))
                self.image2 = self.image2.resize((self.width, self.height))
                self.canvas.config(width=self.width, height=self.height)

            self.update_image(0)

    def on_click(self, event):
        self.start_x = event.x

    def on_drag(self, event):
        position = self.slider_position(event.x)
        self.update_image(position)

    def slider_position(self, x):
        position = x - self.start_x
        position = max(0, position)
        position = min(self.width, position)
        return position

    def update_image(self, position):
        if self.image1 and self.image2:
            comparison = ImageTk.PhotoImage(Image.new('RGB', (self.width, self.height)))
            comparison.paste(self.image2.crop((0, 0, self.width , self.height)), (position, 0))
            comparison.paste(self.image1.crop((0, 0, position, self.height)), (0, 0))
            self.canvas.image = comparison
            self.canvas.create_image(0, 0, anchor=NW, image=comparison)

def main():
    root = Tk()
    root.title('Image Comparison Slider')
    image_slider = ImageSlider(root)
    image_slider.pack(fill=BOTH, expand=True)
    root.mainloop()

if __name__ == '__main__':
    main()
