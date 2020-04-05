import cv2
import numpy as np
from matplotlib import cm

target_image = cv2.imread('./img/mad_penguin.jpg')
marker_colors = []
n_markers = 10
current_marker = 0
marks_updated = False
target_image_copy = np.copy(target_image)
marker_image = np.zeros(target_image.shape[:2],dtype=np.int32)
segments = np.zeros(target_image.shape,dtype=np.uint8)

def setup_marker_colors():
    for i in range(10):
        color = list(cm.tab10(i)[:3])
        color[0] = int(color[0] * 255)
        color[1] = int(color[1] * 255)
        color[2] = int(color[2] * 255)
        color = color[::-1] # This is a bug fix to BGR to RGB behaviour in opencv3
        color = tuple(color)
        marker_colors.append(color)
    
def register_mouse_callback(event, x, y, flags, param):
    global marks_updated 

    if event == cv2.EVENT_LBUTTONDOWN:
        # tracking for markers
        cv2.circle(marker_image, (x, y), 10, (current_marker), -1)
        # DISPLAY ON USER IMAGE
        cv2.circle(target_image_copy, (x, y), 10, marker_colors[current_marker], -1)
        marks_updated = True

if __name__ == "__main__":
    setup_marker_colors()
    cv2.namedWindow('Original Image')
    cv2.setMouseCallback('Original Image', register_mouse_callback)

    while True:
        cv2.imshow('Watershed Segments', segments)
        cv2.imshow('Original Image', target_image_copy)
        
        k = cv2.waitKey(1) & 0xFF

        if k == 27:
            # Close windows with Esc
            break
        elif k == ord('c'):
            # Clear everything
            target_image_copy = np.copy(target_image)
            marker_image = np.zeros(target_image.shape[:2],dtype=np.int32)
            segments = np.zeros(target_image.shape,dtype=np.uint8)
        elif k > 0 and chr(k).isdigit():
            # Pick marker color
            current_marker  = int(chr(k))

        # If we clicked somewhere, call the watershed algorithm on our chosen markers
        if marks_updated:
            marker_image_copy = marker_image.copy()
            cv2.watershed(target_image, marker_image_copy)
            segments = np.zeros(target_image.shape,dtype=np.uint8)

            for color_ind in range(n_markers):
                segments[marker_image_copy == (color_ind)] = marker_colors[color_ind]

            marks_updated = False

    cv2.destroyAllWindows()