import numpy as np
import cv2 as cv

video_file = 'chessboard.avi'
output_file = 'output.avi'
K = np.array([[944.53574431, 0, 345.32015375],
              [0, 876.31371825, 644.90248486],
              [0, 0, 1]])
dist_coeff = np.array([9.49929521e-02, 3.11662831e+00, -3.88910029e-02, -4.50227023e-03, -4.06874417e+01])
board_pattern = (8, 6)
board_cellsize = 0.025
board_criteria = cv.CALIB_CB_ADAPTIVE_THRESH + cv.CALIB_CB_NORMALIZE_IMAGE + cv.CALIB_CB_FAST_CHECK

video = cv.VideoCapture(video_file)
assert video.isOpened(), 'Cannot read the given input, ' + video_file

fps = video.get(cv.CAP_PROP_FPS)
width = int(video.get(cv.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv.CAP_PROP_FRAME_HEIGHT))
fourcc = cv.VideoWriter_fourcc(*'XVID')  
writer = cv.VideoWriter(output_file, fourcc, fps, (width, height))

def create_AR(center=(4.5, 3.5), base=1.0, height=1.0):
    cx, cy = center
    b = base / 2

    pts = [[cx - b, cy - b, 0],
        [cx + b, cy - b, 0],
        [cx + b, cy + b, 0],
        [cx - b, cy + b, 0],
        [cx,     cy,     -height]]
    
    return board_cellsize * np.array(pts, dtype=np.float32)

AR_points = create_AR()

obj_points = board_cellsize * np.array([[c, r, 0] for r in range(board_pattern[1]) for c in range(board_pattern[0])])

while True:

    valid, img = video.read()
    if not valid:
        break

    success, img_points = cv.findChessboardCorners(img, board_pattern, board_criteria)
    if success:
        ret, rvec, tvec = cv.solvePnP(obj_points, img_points, K, dist_coeff)

        proj_AR, _ = cv.projectPoints(AR_points, rvec, tvec, K, dist_coeff)
        proj_AR = np.int32(proj_AR).reshape(-1, 2)

        for i in range(4):cv.line(img, proj_AR[i], proj_AR[(i + 1) % 4], (255, 255, 0), 2)
        for i in range(4):cv.line(img, proj_AR[i], proj_AR[4], (0, 0, 255), 2)

        R, _ = cv.Rodrigues(rvec) 
        p = (-R.T @ tvec).flatten()
        info = f'XYZ: [{p[0]:.3f} {p[1]:.3f} {p[2]:.3f}]'
        cv.putText(img, info, (10, 25), cv.FONT_HERSHEY_DUPLEX, 0.6, (0, 255, 0))
        
    writer.write(img)

    cv.imshow('Pose Estimation (Chessboard)', img)
    key = cv.waitKey(10)
    if key == ord(' '):
        key = cv.waitKey()
    if key == 27: 
        break

video.release()
writer.release()
cv.destroyAllWindows()