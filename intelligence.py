# This is a template.
# You should modify the functions below to match
# the signatures determined by the project specification
from matplotlib import pyplot as mat_plot
import numpy as np


# import intelligence


def find_red_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """
        finds all red pixels in a png and returns a jpeg

        Args:
            map_filename: name of the file to find pixels in
            upper_threshold (int): upper limit of specific RGB value
            lower_threshold (int): lower limit of specific RGB value

        Returns:
            (2d ndarray): contains all red pixels in the image as a black and white jpeg

        """
    mat_plot.axis('off')
    rgb_img = mat_plot.imread(map_filename)  # opens file
    new_image = []
    for row in range(rgb_img.shape[0]):  # loops through number of rows in image
        temp = []
        for pixel in range(rgb_img.shape[1]):  # loops through each pixel (columns)
            r = rgb_img[row][pixel][0] * 255  # adjusting colour values (scaling)
            g = rgb_img[row][pixel][1] * 255
            b = rgb_img[row][pixel][2] * 255
            if g < lower_threshold and b < lower_threshold and r > upper_threshold:  # checks within thresholds
                temp.append(np.array([255, 255, 255]).astype(float))  # add to white pixel if it is
            else:
                temp.append(np.array([0, 0, 0]).astype(float))  # add black pixel if not
        new_image.append(temp)  # add row to array
    new_image = np.array(new_image).astype(float)
    mat_plot.imsave("map-red-pixels.jpg", new_image.astype(np.uint8))  # save as a jpeg image using matplotlib
    return new_image


def find_cyan_pixels(map_filename, upper_threshold=100, lower_threshold=50):
    """
    finds all cyan pixels in a png and returns a jpeg

    Args:
        map_filename: name of the file to find pixels in
        upper_threshold (int): upper limit of specific RGB value
        lower_threshold (int): lower limit of specific RGB value

    Returns:
        (2d ndarray): contains all cyan pixels in the image as a black and white jpeg

    """
    mat_plot.axis('off')
    rgb_img = mat_plot.imread(map_filename)  # opens file
    new_image = []
    for row in range(rgb_img.shape[0]):  # loops through number of rows in image
        temp = []
        for pixel in range(rgb_img.shape[1]):  # loops through each pixel (columns)
            r = rgb_img[row][pixel][0] * 255  # adjusting colour values (scaling)
            g = rgb_img[row][pixel][1] * 255
            b = rgb_img[row][pixel][2] * 255
            if g > upper_threshold and b > upper_threshold and r < lower_threshold:  # checks within thresholds
                temp.append(np.array([255, 255, 255]).astype(float))  # add to white pixel if it is
            else:
                temp.append(np.array([0, 0, 0]).astype(float))  # add black pixel if not
        new_image.append(temp)  # add row to array
    new_image = np.array(new_image).astype(float)
    mat_plot.imsave("map-cyan-pixels.jpg", new_image.astype(np.uint8))  # save as a jpeg image using matplotlib
    return new_image


def enqueue(queue, item):
    """
    adds an item to the queue

    Args:
        queue (ndarray) : current queue to add to
        item (string) : item to add to queue

    Returns:
        (ndarray): edited queue

    """
    queue = np.append(queue, item)
    return queue


def dequeue(queue):
    """
    dequeues an item from a given queue

    Args:
        queue: queue to remove item from

    Returns:
        (string): item that has been dequeued
        (ndarray): queue that has been edited

    """
    item = queue[0]
    for i in range(len(queue) - 1):
        queue[i] = queue[i + 1]
    queue = np.delete(queue, len(queue) - 1)  # deletes last item in queue
    return item, queue


def is_empty(queue):
    """
    checks whether the given queue is empty

    Args:
        queue (ndarray): queue being checked

    Returns:
        (bool): boolean value for whether the queue is empty or not

    """
    if len(queue) == 0:
        return True
    else:
        return False


def detect_connected_components(img):
    """
    reads IMG returned from Task MI-1 (DOESN'T WORK)

    Args:
        img: a 2D array containing pixels with RGB values

    Returns: returns a 2D array in numpy MARK and writes the number of pixels inside each connected component
    region into a text file cc-output-2a.txt

    """
    Q = np.array([])
    MARK = np.zeros((img.shape[0], img.shape[1]))
    connected_component_counter = 0
    pixel_counter = 0
    output = {}
    x = -1
    for row in img:  # starting from top left corner, row by row scanning
        x += 1
        y = -1
        for pixel in row:
            y += 1
            # if np.logical_and(255, pixel):
            if img[x, y][0] > 200 and img[x, y][1] > 200 and img[x, y][2] > 200 and MARK[x, y] == 0: # checks if pixel is a pavement pixel and it is not visited
                MARK[x, y] = 1 # sets to visited
                Q = enqueue(Q, img[x, y]) # adds pixel to queue
                while not is_empty(Q):
                    (item, Q) = dequeue(Q)  # takes item out the queue
                    pixel_counter += 1  # adds a pixel every time an item is dequeued
                    for m in range(1, 3):  # finds 8-connected components and assigns x and y values to the position
                        for n in range(1, 3):
                            s = 0
                            t = 0
                            if m == 1:
                                s = x + 1
                            elif m == 2:
                                s = x
                            elif m == 3:
                                s = x - 1

                            if n == 1:
                                t = y + 1
                            elif n == 2:
                                t = y
                            elif n == 3:
                                t = y - 1

                            if (0 < t < 1053) and (0 < s < 1140):  # checks it is within the bounds
                                # img[s, t].all() == np.array([255, 255, 255]).all()
                                if img[s, t][0] > 200 and img[s, t][1] > 200 and img[s, t][2] > 200 and (m, n) != (
                                2, 2):  # checks if it is a pavement pixel and not the current pixel
                                    if MARK[s, t] == 0:
                                        MARK[s, t] = 1  # marks as visited
                                        enqueue(Q, img[s, t]) # queues the pixel
                output[connected_component_counter] = pixel_counter
                connected_component_counter += 1
                pixel_counter = 0

    for key in output:
        print("Connected Component: " + str(key) + " Number of pixels: " + str(output[key])) # prints connected components

    return MARK


#  detect_connected_components(find_red_pixels("data\map.png"))


def detect_connected_components_sorted(MARK):
    """
    Args:
        MARK: list of connected components

    Returns: not completed, should be an image and a text file

    """

    MARK = Bubble_Sort(MARK)
    f = open("test/cc-output-2b.txt", "w")
    f.write(str(MARK))
    f.close()
    # Doesn't work, ran out of time
    # MARK_SAVE = np.array([])
    # np.append(MARK_SAVE, MARK[0])
    # np.append(MARK_SAVE, MARK[1])
    # mat_plot.imsave("cc-top-2.jpg", MARK_SAVE.astype(np.uint8))


def Bubble_Sort(MARK):
    n = len(MARK)
    swapped = False
    # Goes through all array elements
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if MARK[j][0] < MARK[j + 1][0]:  # if element is less than the one after it, swap
                swapped = True
                MARK[j], MARK[j + 1] = MARK[j + 1], MARK[j]

        if not swapped:
            return

    return MARK
