# Use this file to write your filter functions!

# Note for AddisCoder: These filters operate on 3D arrays: image[row][column] = [r, g, b]
# I found this was a bit confusing when I taught this before, so have reworked the lectures
# to use the SimpleImage image.get_pixel(x, y) and image.set_pixel(x, y, r, g, b) APIs.

# Thus the algorithms here still work, but need to be re-written to use the image API.
import copy

def red_stripes(image_matrix):
    new_matrix = image_matrix.copy()
    for x in range(len(new_matrix)):
        if (x // 50) % 2 == 0:
            new_matrix[x] = [[255, r[1], r[2]] for r in image_matrix[x]]
    return new_matrix

def grayscale(image_matrix):
    new_matrix = image_matrix.copy()
    for x in range(len(new_matrix)):
        for y in range(len(new_matrix[x])):
            avg = int(sum(image_matrix[x][y]) / 3)
            new_matrix[x][y] = [avg, avg, avg]
    return new_matrix

def invert_colors(image_matrix):
    new_matrix = image_matrix.copy()
    for x in range(len(new_matrix)):
        for y in range(len(new_matrix[x])):
            pixel = new_matrix[x][y]
            new_matrix[x][y] = [255 - pixel[0], 255 - pixel[1], 255 - pixel[2]]
    return new_matrix

def flip(image_matrix):
    new_matrix = image_matrix.copy()
    for x in range(int(len(new_matrix) / 2)):
        flip_index = len(new_matrix) - 1 - x
        temp_list = list(new_matrix[x])
        new_matrix[x] = list(new_matrix[flip_index])
        new_matrix[flip_index] = temp_list
    return new_matrix

def blur(image_matrix):
    new_matrix = copy.deepcopy(image_matrix)
    for x in range(len(new_matrix)):
        for y in range(len(new_matrix[0])):
            pixel = image_matrix[x][y]
            neighbors = [pixel]
            if x != 0:
                if y != 0:
                    neighbors.append(image_matrix[x - 1][y - 1])
                if y != len(new_matrix[0]) - 1:
                    neighbors.append(image_matrix[x - 1][y + 1])
                neighbors.append(image_matrix[x - 1][y])
            if x != len(new_matrix) - 1:
                if y != 0:
                    neighbors.append(image_matrix[x + 1][y - 1])
                if y != len(image_matrix[0]) - 1:
                    neighbors.append(image_matrix[x + 1][y + 1])
                neighbors.append(image_matrix[x + 1][y])
            if y != 0:
                neighbors.append(image_matrix[x][y - 1])
            if y != len(image_matrix[0]) - 1:
                neighbors.append(image_matrix[x][y + 1])
            rgb_list = [0, 0, 0]
            for neighbor in neighbors:
                rgb_list[0] += neighbor[0]
                rgb_list[1] += neighbor[1]
                rgb_list[2] += neighbor[2]
            rgb_avg = [e // len(neighbors) for e in rgb_list]
            new_matrix[x][y] = (rgb_avg)
    return new_matrix

def sepia(image_matrix):
    new_matrix = copy.deepcopy(image_matrix)
    for x in range(len(new_matrix)):
        for y in range(len(new_matrix[0])):
            input_red, input_green, input_blue = new_matrix[x][y]
            output_red = min(255, int((input_red * .393) + (input_green *.769) + (input_blue * .189)))
            output_green = min(255, int((input_red * .349) + (input_green *.686) + (input_blue * .168)))
            output_blue = min(255, int((input_red * .272) + (input_green *.534) + (input_blue * .131)))
            new_matrix[x][y] = [output_red, output_green, output_blue]
    return new_matrix


def threshold(image_matrix,
              red_threshold=(0, 255),
              green_threshold=(0, 255),
              blue_threshold=(0, 255)):
    new_matrix = image_matrix.copy()
    for x in range(len(new_matrix)):
        for y in range(len(new_matrix[0])):
            pixel = new_matrix[x][y]
            in_red_thresh = pixel[0] >= red_threshold[0] and pixel[0] <= red_threshold[1]
            in_green_thresh = pixel[1] >= green_threshold[0] and pixel[1] <= green_threshold[1]
            in_blue_thresh = pixel[2] >= blue_threshold[0] and pixel[2] <= blue_threshold[1]
            if not(in_red_thresh and in_green_thresh and in_blue_thresh):
                new_matrix[x][y] = [0, 0, 0]
    return new_matrix