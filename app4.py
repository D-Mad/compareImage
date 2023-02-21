from tkinter import *
from PIL import Image, ImageTk

class ImageSlider(Frame):
    def __init__(self, master, image1, image2):
        super().__init__(master)

        self.image1 = Image.open(image1)
        self.image2 = Image.open(image2)

        self.width, self.height = self.image1.size

        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

        self.canvas.bind('<Button-1>', self.on_click)
        self.canvas.bind('<B1-Motion>', self.on_drag)

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
        comparison = ImageTk.PhotoImage(Image.new('RGB', (self.width, self.height)))
        comparison.paste(self.image2.crop((0, 0, self.width , self.height)), (position, 0))
        comparison.paste(self.image1.crop((0, 0, position, self.height)), (0, 0))
        self.canvas.image = comparison
        self.canvas.create_image(0, 0, anchor=NW, image=comparison)

def main():
    root = Tk()
    root.title('Image Comparison Slider')
    image_slider = ImageSlider(root, 'image1.jpg', 'image2.jpg')
    image_slider.pack(fill=BOTH, expand=True)
    root.mainloop()

if __name__ == '__main__':
    main()
