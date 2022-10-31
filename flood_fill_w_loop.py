import cv2
import numpy as np

class FloodFiller:
    def __init__(self, img: np.ndarray, tolerance: int):
        # the original image, will not be changed
        self.img = img

        # the hue tolerance for the flood fill
        self.tolerance = tolerance
        
        # create a copy of the image to draw on
        self.img_copy = img.copy()

        # create an HSV version of the image so that we can compare hue values
        # will not be changed, only referenced
        self.hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # create a blank matrix to record filled pixels
        height = img.shape[0]
        width = img.shape[1]
        self.pixel_fill_matrix = np.zeros((height, width), dtype = "uint8")

        # initialize the fill color
        self.fill_color = np.array([0,0,255])
        self.iteration = 0 # for adjusting the fill color

    def check_tolerance(self, x: int, y: int) -> bool:
        """
        Checks a specified pixel and determines if it is within acceptable 
        tolerance, i.e. close enough to the target hue

        x: the x coordinate of the pixel of which the tolerance will be checked
        y: the y coordinate ...
        """

        hue = self.hsv_img[y][x][0] 
        
        return hue >= self.hue_min and hue <= self.hue_max
      
    def fill_pixel(self, x: int, y: int) -> None:
        """
        Fills a single pixel.
        x: x coordinate of the pixel
        y: y coordinate...
        """
        self.img_copy[y][x] = self.fill_color
        self.pixel_fill_matrix[y][x] = 1

    def run(self):
        """
        This method should be called iteratively within a main loop.
        Each iteration fills a few more pixels and returns the resulting image
        and is_finished (bool).
        When is_finished = True, the image has been completed filled.
        """
        # define the relative positions of the nearby pixels to check
        positions_to_check = [
            [-1,0], # left
            # [-1,1], # upper left
            [0,1],  # above
            # [1,1],  # upper right
            [1,0],  # right
            # [1,-1],  # lower right
            [0,-1], # below
            # [-1,-1], # lower left
        ]

        # EXPERIMENTING WITH DIFFERENT COLOR SCHEMES
        red = self.fill_color[2]
        red -= 1
        if red < 0:
            red = 250

        if self.iteration % 10 == 0:
            green = 0
            blue = 255
        else:
            green = 255
            blue = 0

        self.fill_color = np.array([blue,green,red])

        # update the sets
        self.pixels_to_fill_current = self.pixels_to_fill_next.copy()
        self.pixels_to_fill_next = set([])

        for pixel in self.pixels_to_fill_current:
            # fill the pixel
            self.fill_pixel(pixel[0], pixel[1])

            # check which nearby pixels need to be filled
            for position in positions_to_check:
                x_coord = pixel[0] + position[0]
                y_coord = pixel[1] + position[1]

                # check if the new position is out of bounds
                if x_coord > (self.img.shape[1] - 1) or x_coord < 0:
                    continue
                if y_coord > (self.img.shape[0] - 1) or y_coord < 0:
                    continue

                # check if the pixel is already filled
                if self.pixel_fill_matrix[y_coord][x_coord]:
                    # do not fill the pixel if it has already been filled
                    continue
                
                # check if the pixel is within tolerance
                is_with_tolerance = self.check_tolerance(x_coord, y_coord)
                if is_with_tolerance:
                    self.pixels_to_fill_next.add((x_coord, y_coord))

        if self.pixels_to_fill_next:
            is_finished = False
        else:
            is_finished = True

        self.iteration += 1

        return is_finished, self.img_copy

    def click(self, x: int, y: int):
        """
        Sets the (x, y) coordinates from which the flood fill will occur
        """
        # initialize the lists for keeping track of pixels to check
        self.pixels_to_fill_current = set([])
        self.pixels_to_fill_next = set([(x, y)])

        # set the hue range
        self.hue_max = self.hsv_img[y][x][0] + self.tolerance
        self.hue_min = self.hsv_img[y][x][0] - self.tolerance

def main():
    from timeit import default_timer as timer
    from time import sleep
    import random

    # constants
    tolerance = 7

    # read the image
    path = 'sky.png'
    img = cv2.imread(path)

    run = True
    while run:
        # initialize the FloodFiller object
        flood_filler = FloodFiller(img, tolerance)

        # click somewhere on the image
        center_x = random.randint(0, img.shape[1] - 1)
        center_y = random.randint(0, img.shape[0] - 1)
        flood_filler.click(center_x, center_y)

        t1 = timer()
        while run:
            is_finished, img_copy = flood_filler.run()

            # cv2.circle(img_copy, (center_x, center_y), (6), (255,0,0), -1)
            cv2.imshow('img_copy', img_copy)
            
            if is_finished:
                break

            # check pressed keys 
            key = cv2.waitKey(1)
            if key == ord('q'):
                run = False
    
        print('Finished!') 

        # stop the timer
        t2 = timer()
        elapsed_time = t2 - t1 
        print(f'elapsed_time: {elapsed_time}')

        # show the final result
        cv2.imshow('img_copy', img_copy)  
        cv2.waitKey(2000)

    # clean up
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()



