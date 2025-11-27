# Tính được mm trên thước chuẩn

import cv2
import numpy as np

from imgLoad import loadImage

points = []

# Hàm đẩy các điểm click chuột vào list
def mouse_callback(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:# Sự kiện nhấp chuột trái
        points.append((x, y))# Đẩy tọa độ vào list
        #print('Point cordinate: ', (x, y))


def select_segment(img):
    global points
    points = []

    # Tạo window để gán callback chuột
    cv2.namedWindow('Select 2 straight point')
    cv2.setMouseCallback("Select 2 straight point", mouse_callback)

    while True:
        temp = img.copy()

        # Vẽ điểm user đã chọn
        for p in points:
            cv2.circle(temp, p, 5, (0, 0, 255), -1)

        # Nếu chọn được 2 điểm thì vẽ line
        if len(points) == 2:
            cv2.line(temp, points[0], points[1], (0, 0, 0), 1)

        cv2.imshow("Select 2 straight point", temp)
        key = cv2.waitKey(1)

        # Dừng khi esc
        if key == 27:
            cv2.destroyAllWindows()
            return None, None
        
        # Chỉ cho phép chọn 2 điểm
        if len(points) == 2:
            break

    cv2.destroyAllWindows()

    # Tính khoảng cách
    p1, p2 = points[0], points[1]
    # Hàm tính khoảng cách euclid giữa hai tọa độ pixel
    pixel_distance = np.linalg.norm(np.array(p1) - np.array(p2))

    return pixel_distance

def compute_mm_per_pixel(pixel_dist, real_mm):
    return real_mm / pixel_dist

def show_ruler_and_get_scale(ruler_img):
    pixel_dist = select_segment(ruler_img)

    if pixel_dist == (None, None):
        print('Cancelled')
        return None

    #print('Pixel length: ', pixel_dist)

    real_mm = float(input("Nhập độ dài thật (mm): "))
    mm_per_pixel = compute_mm_per_pixel(pixel_dist, real_mm)

    print('mm_per_pixel =', mm_per_pixel)

    return mm_per_pixel


# ruler, obj, full = loadImage("./imgs/earphone.jpg")

# mmpp = show_ruler_and_get_scale(ruler)

