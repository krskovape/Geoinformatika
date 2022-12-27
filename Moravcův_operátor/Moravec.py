from PIL import Image, ImageOps
from math import inf
from matplotlib import pyplot as plt

# function to open image and convert it to grayscale
def open_image(image):
    try:
        with Image.open(image) as im:
            return ImageOps.grayscale(im)
    except FileNotFoundError:
        print(f"Cannot open file. The file does not exist or the path to the file is incorrect.")
        quit()
    except PermissionError:
        print(f"Program doesn't have permisson to acces file.")
        quit()
    except Exception as e:
        print(f"Unexpected error opening file: {e}")
        quit()

# function to create window of given size
def create_window(window_size, vectors):
    # number to multiply vectors
    m = int((window_size + 1) / 2) - 1

    # create the window by copying the list of vectors and adding central pixel
    window = vectors.copy()
    window.append([0,0])

    # check if the window size is an odd number and bigger than 3
    if window_size % 2 == 0:
        print("The window size must be an odd number.")
        quit()
    elif window_size < 3:
        print("The window size must be bigger than 3.")
        quit() 
    else:
        # add coordinates of all pixels in the window of given size to window list
        for k in range(2,m+1):
            for item in vectors:
                vx = item[0]
                vy = item[1]
                window.append([vx*k, vy*k])
                if abs(vx) == abs(vy):
                    for i in range (1,k):
                        window.append([item[0]*k, item[1]*i])
                        window.append([item[0]*i, item[1]*k])
    return window, m

# Moravec operator
def moravec(image, window_size, treshold):
    # open image
    im = open_image(image)

    # list of vectors for matrix 3x3
    vector = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]]
    
    # create window
    window, m = create_window(window_size, vector)

    # create empty list of edge points coordinates
    edge_points = []
    edge_x = []
    edge_y = []

    # iterate over columns and rows in image
    for col in range(m,im.size[0]):
        for row in range(m,im.size[1]):
            # initialize property of the minimum difference to infinity
            E_min = inf

            # place the centre of the window over the current pixel
            # iterate over all pixels in the window
            for p in window:
                px = col + p[0]
                py = row + p[1]

                # initialize the sum of the squared pixel differences to zero
                sum_diff = 0

                # check if the window´s pixel is not out of the image / grid, otherwise continue to the next window´s pixel
                if px < 0 or py < 0 or px > im.size[0] - 1 or py > im.size[1] - 1:
                    continue
                
                # move the window´s pixel in every direction given by v in list of vectors
                for v in vector:
                    # check if the moved pixel is not out of the image / grid, otherwise move to the next pixel
                    if (px + v[0]) < 0 or (py + v[1]) < 0 or (px + v[0]) > im.size[0] - 1 or (py + v[1]) > im.size[1] - 1:
                        continue
                    
                    # calculate squared difference of pixel values and add it to the sum
                    sq_diff = ((im.getpixel((px + v[0], py + v[1]))) - (im.getpixel((px, py))))**2
                    sum_diff += sq_diff

                # if the sum of the squared differences is lower than the minimum, overwrite it
                if sum_diff < E_min:
                    E_min = sum_diff
            
            # if the minimum of sum of the squared differences is greater than given treshold, add its coordinates to given list
            if E_min >= treshold:
                edge_points.append([col, row])
                edge_x.append([col])
                edge_y.append([row])

    return edge_points, edge_x, edge_y

# function to vizualize the original pixtures and detected edge points
def vizu_edges(image, edge_coord_x, edge_coord_y):
    with Image.open(image) as im:
        plt.imshow(im)
        plt.scatter(edge_coord_x, edge_coord_y, c='r', s=2)
        plt.show()

# write coordinates of edge points info file
def write_to_file(edge_points, output_file):
    with open(output_file, "w") as f:
        for i in edge_points:
            line = str(i[0]) + ", " + str(i[1])
            f.write(line)
            f.write("\n")

# arguments for the functions
# directory to image
image = "lena.tif"
# window size (3 for 3x3 window)
window_size = 3
# treshold for edge points
treshold = 3500
# directory to output file to write the results into
output_file = "output.txt"

# calculate coordinates of the edge points (edge_x and edge_y are needed only for the vizualization)
edge_points, edge_x, edge_y = moravec(image, window_size, treshold)

# write the coordinates of the edge points into file
write_to_file(edge_points, output_file)

# vizualize edge points over the original image
vizu_edges(image, edge_x, edge_y)