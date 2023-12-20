import cv2
import numpy as np
import pickle

import numpy as np

def get_real_world_coordinates(grid_size, rows, columns):
    real_world_points = []
    for row in range(rows):
        for col in range(columns):
            x = col * grid_size  # X-coordinate in centimeters
            y = row * grid_size  # Y-coordinate in centimeters
            real_world_points.append([x, y, 0])
    return np.array(real_world_points, dtype=np.float32)

# Example usage:
grid_size = 2.5  # Size of each square in centimeters
rows = 7         # Number of rows in the checkerboard grid
columns = 9      # Number of columns in the checkerboard grid



# Load the camera matrix and distortion coefficients from the .pkl file
with open('calibration.pkl', 'rb') as file:
    calibration_data = pickle.load(file)

camera_matrix = calibration_data[0]
distortion_coefficients = calibration_data[1]

# Load your image for calibration
image = cv2.imread(r'C:\Users\Shirshak\Desktop\Robotics Summer Project\Photos\Paths\path5.png')


# Undistort the image using the loaded camera matrix and distortion coefficients
undistorted_image = cv2.undistort(image, camera_matrix, distortion_coefficients)

# Extract pixel coordinates of calibration markers/features from the undistorted image
# pixel_coordinates = get_pixel_coordinates(undistorted_image)

grid_size=2.5
rows=10
columns=20
def Get_World_Coords(path_in_pixels):
    pixel_coords=np.array(path_in_pixels,dtype=np.float32)
    pixel_coordinates=np.array([[0,0],[6240,0],[6240,3691],[0,3691]], dtype=np.float32)

# real_world_coordinates = get_real_world_coordinates(grid_size,rows,columns)
    real_world_coordinates=np.array([[0,0],[542,0],[542,321],[0,321]], dtype=np.float32)
# print(real_world_coordinates)

# Calculate the transformation matrix
    transformation_matrix,_= cv2.findHomography(pixel_coordinates, real_world_coordinates)
    real_world_coord = cv2.perspectiveTransform(np.array([pixel_coords], dtype=np.float32), transformation_matrix)
    return real_world_coord

