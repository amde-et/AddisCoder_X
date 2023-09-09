"""
SimpleImage is a module written for AddisCoder 2023 by Alexander Krentsel,
and is heavily based on the SimpleImage module written for CS106A at Stanford
University, but has been modified to simplify the interface for students
and better handle working with small canvases.

For students: do not worry yet about what is in this file. For now, you
can think of SimpleImage as a custom complex type that we have created for
you. We will not discuss how to create custom types (called "classes")
during AddisCoder, but you will learn about them in a future 

SimpleImage Features:
Create image:
  image = SimpleImage.blank(400, 200)   # create new image of size
  image = SimpleImage('foo.jpg')        # create from file

Access size:
  image.width, image.height

Get pixel at x,y (0,0 is the top left corner):
  pix = image.get_rgb(x, y)
  # pix is an RGB list like [100, 200, 0], where the color components of the
  # pixel are Red = 100, Green = 200, and Blue = 0.

Set pixel at x,y:
  image.set_rgb(x, y, r, g, b)

Show image on screen:
  image.show()

Show a small image zoomed-in (larger) so it's easier to see the pixels:
  image.show(resize_width=400)

The main() function below demonstrates the above functions.
"""

import sys
# If the following line fails, "Pillow" needs to be installed. Ask your
# TA for help.
from PIL import Image


def clamp(num):
    """
    Return a "clamped" version of the given num,
    converted to be an int limited to the range 0..255.
    """
    num = int(num)
    if num < 0:
        return 0
    if num >= 256:
        return 255
    return num


# color tuples for background color names 'red' 'white' etc.
BACK_COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
}


class SimpleImage(object):
    def __init__(self, filename, width=0, height=0, back_color=None):
        """
        Create a new image. This case works: SimpleImage('foo.jpg')
        To create a blank image use SimpleImage.blank(500, 300)
        The other parameters here are for internal/experimental use.
        """
        # Create pil_image either from file, or making blank
        if filename:
            self.pil_image = Image.open(filename).convert("RGB")
            if self.pil_image.mode != 'RGB':
                raise Exception('Image file is not RGB')
            self._filename = filename  # hold onto
        else:
            if not back_color:
                back_color = 'white'
            color_tuple = BACK_COLORS[back_color]
            if width == 0 or height == 0:
                raise Exception('Creating blank image requires width/height but got {} {}'
                                .format(width, height))
            self.pil_image = Image.new('RGB', (width, height), color_tuple)
        self.px = self.pil_image.load()
        size = self.pil_image.size
        self._width = size[0]
        self._height = size[1]
        self.curr_x = 0
        self.curr_y = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.curr_x < self.width and self.curr_y < self.height:
            x = self.curr_x
            y = self.curr_y
            self.increment_curr_counters()
            return self.get_rgb(x, y)
        else:
            self.curr_x = 0
            self.curr_y = 0
            raise StopIteration()

    def increment_curr_counters(self):
        self.curr_x += 1
        if self.curr_x == self.width:
            self.curr_x = 0
            self.curr_y += 1

    @classmethod
    def blank(cls, width, height, back_color=None):
        """Create a new blank image of the given width and height, optional back_color."""
        return SimpleImage('', width, height, back_color=back_color)

    @classmethod
    def file(cls, filename):
        """Create a new image based on a file, alternative to raw constructor."""
        return SimpleImage(filename)

    @property
    def width(self):
        """Width of image in pixels."""
        return self._width

    @property
    def height(self):
        """Height of image in pixels."""
        return self._height

    def set_rgb(self, x, y, red, green, blue):
        """
        Set the pixel at the given x,y to have
        the given red/green/blue values without
        requiring a separate pixel object.
        """
        self.px[x, y] = (red, green, blue)
    
    def get_rgb(self, x, y):
        """
        Returns a list of [red, green, blue] values
        for the pixel at the given x,y.
        """
        return list(self.px[x, y])

    def show(self, resize_width=None):
        """Displays the image using an external utility. Blows up the image if it is too small."""
        
        if resize_width is not None:
            # if a resize_width is specified, resize the image before displaying.
            new_img = self.pil_image.resize((resize_width, int((float(resize_width) / self.width) * self.height)), Image.Resampling.BOX)
            display(new_img)
            return
        
        display(self.pil_image)


def main():
    """
    main() exercises the features as a test.
    1. With 1 arg like `images/castle.jpeg` - opens it
    2. With 0 args, creates a yellow square with
    a green stripe at the right edge.
    """
    args = sys.argv[1:]
    if len(args) == 1:
        image = SimpleImage.file(args[0])
        image.show()
        return

    # Create yellow rectangle.
    image = SimpleImage.blank(400, 200)
    for x in range(image.width):
        for y in range(image.height):
            image.set_rgb(x, y, 255, 255, 0)

    # Set green stripe.
    pixel = image.get_rgb(0, 0)
    green = pixel[1]  # [r, g, b]
    for x in range(image.width - 10, image.width):
        for y in range(image.height):
            image.set_rgb(x, y, 0, green, 0)
    image.show()


if __name__ == '__main__':
    main()