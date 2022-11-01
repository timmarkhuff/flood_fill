import cv2
import numpy as np
import random

class Pixel:
    """This function keeps track of the color of the pixels in the target image 
    This is Eric, and I also agree with Darius' aforementioned clarification"""
    
    
    def __init__(self, x:int, y:int, img:np.ndarray):
        self.x = x
        self.y = y
        self.img = img
        self.value = img[y][x]

    def fill(self, img, fill_color):
        img[self.y][self.x] = fill_color        
        # draw an animation
        if random.randint(0,100) > 10:
            # resize the image
            img_to_show = cv2.resize(img, (300,300))
            cv2.imshow('img_to_show', img_to_show)
            cv2.waitKey(1)

#check the tolerance
def check_tolerance(tolerance:int,
                    target_pixel:Pixel, 
                    current_pixel:Pixel, 
                    ) -> bool:
    for n, channel in enumerate(current_pixel.value):
        if abs(int(channel) - int(target_pixel.value[n])) > tolerance:
            return False
    return True

#add new piexls unsearched
def find_adjacent_pixels_to_fill(tolerance:int,
                                target_pixel:Pixel,
                                current_pixel:Pixel,
                                ):
    positions_to_check = [
        [-1,0], # pixel to the left
        [0,1], # above
        [1,0], # right
        [0,-1], # below
    ]

    adjacent_pixels_to_fill = []
    for position in positions_to_check:
        # define coordinates of new pixel
        x = position[0] + current_pixel.x
        y = position[1] + current_pixel.y

        # check if the pixel is out of bounds
        image_width = current_pixel.img.shape[1]
        if x > image_width - 1 or x < 0:
            continue # skip this point if out of bounds
        image_height = current_pixel.img.shape[0]
        if y > image_height - 1 or y < 0:
            continue # skip this point if out of bounds

        # create the new pixel
        new_pixel = Pixel(x, y, current_pixel.img)
        
        # check if the color is close enough to the target pixel value (based on tolerance)
        within_tolerance = check_tolerance(tolerance, target_pixel, new_pixel)
        if within_tolerance:
            adjacent_pixels_to_fill.append(new_pixel)
    
    return adjacent_pixels_to_fill

#main function of floodfill
def flood_fill(img:np.ndarray, 
               img_copy:np.ndarray, 
               tolerance:int,
               fill_color:tuple,
               target_pixel:Pixel, 
               current_pixel:Pixel=None
               ) -> np.ndarray:

    # If no current pixel was provided, set it equal to the target_pixel
    # This is for the first level of recursion
    if not current_pixel:
        current_pixel = target_pixel

    # fill the current pixel with red
    current_pixel.fill(img_copy, fill_color)

    # find adjacent pixels that need to be filled
    adjacent_pixels_to_fill = find_adjacent_pixels_to_fill(tolerance, target_pixel, current_pixel)

    # if there are no pixels to fill, terminate recursion
    if not adjacent_pixels_to_fill:
        return
        
    # fill all the pixels that need to be filled, use recursion
    for adjacent_pixel_to_fill in adjacent_pixels_to_fill:
        if list(img_copy[adjacent_pixel_to_fill.y][adjacent_pixel_to_fill.x]) == list(fill_color):
            # don't fill the pixel if it has already been filled
            continue
        flood_fill(img, img_copy, tolerance, fill_color, target_pixel, adjacent_pixel_to_fill)

def main():
    
    # increase the maximum recusion depth limit
    import sys
    sys.setrecursionlimit(1000000)

    # constants
    TOLERANCE = 30
    FILL_COLOR = np.array([0,137,255])

    # define the image
    img_url = r"C:\Users\Owner\Documents\Dropbox\GIX\MSTI\TECHIN509 - Tech Fundamentals\flood_fill\sky.png"
    img = cv2.imread(img_url)

    # resize the image
    # img = cv2.resize(img, (75,75))

    # copy the image
    img_copy = img.copy()

    # create a target pixel (the pixel that was clicked)
    target_x = 200
    target_y = 20
    target_pixel = Pixel(target_x, target_y, img)

    # apply the flood fill function
    flood_fill(img, img_copy, TOLERANCE, FILL_COLOR, target_pixel)
    print('Finished flood_fill!')      

    cv2.circle(img_copy, (target_x,target_y), 5, (255,0,0),2)
    
    # show results
    cv2.imshow('img', img_copy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
    main()

