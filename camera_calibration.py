import cv2 as cv
import numpy as np

def select_img_from_video(video_file, board_pattern, select_all=False, wait_msec=10):

    video = cv.VideoCapture(video_file)
    img_select = []
    while True:
        valid, img = video.read()
        if not valid:
            break
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        complete, _ = cv.findChessboardCorners(gray, board_pattern)
        if complete:
            img_select.append(img)
        if not select_all:
            break
    return img_select

def calib_camera_from_chessboard(images, board_pattern, board_cellsize, K=None, dist_coeff=None, calib_flags=None):
    img_points = []
    for img in images:
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        complete, pts = cv.findChessboardCorners(gray, board_pattern)
        if complete:
            img_points.append(pts)
    assert len(img_points) > 0, 'No valid chessboard images found!'
    obj_pts = [[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])]
    obj_points = [np.array(obj_pts, dtype=np.float32) * board_cellsize] * len(img_points)
    
    ret, K, dist_coeff, rvecs, tvecs = cv.calibrateCamera(obj_points, img_points, gray.shape[::-1], K, dist_coeff, flags=calib_flags)
    
    print("Camera Matrix (K):\n", K)
    print("Distortion Coefficients:\n", dist_coeff)
    print("Reprojection Error:", ret)
    
    return ret, K, dist_coeff, rvecs, tvecs

if __name__ == "__main__":
    video_file = "chessboard.avi"
    board_pattern = (8, 6)
    board_cellsize = 0.025 
    images = select_img_from_video(video_file, board_pattern, select_all=True)
    calib_camera_from_chessboard(images, board_pattern, board_cellsize)
