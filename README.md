# my_camera_pose_estimation_AR

해당 프로젝트는 Opencv를 활용한 간단하게 Camera Calibration 및 Pose Estimation, AR object visualization을 할 수 있는 Python 프로그램입니다.

## Camera Calibration  결과

체스보드 패턴을 이용해 OpenCV의 Calibration 기능을 사용하여 Camera Calibration을 수행했습니다. 얻어진 내부 파라미터 및 왜곡 계수는 다음과 같습니다.
| 파라미터 | 값 |
| ------ | ------ |
| K | [[944.53574431 ,  0 ,  345.32015375] [0 ,      876.31371825 , 644.90248486] [0 , 0 , 1]] |
| Distortion Coefficients | [[ 9.49929521e-02 , 3.11662831e+00 , -3.88910029e-02  , -4.50227023e-03  , -4.06874417e+01]] |
| Reprojection Error | 1.2006559540450095 |

## AR 결과 데모

위에서 얻은 Calibration 데이터를 활용해 Camera pose estimation 및 AR object visualization을 진행하였습니다. AR 물체가 표시된 영상은 output.avi 파일로 저장되었습니다.

![Image](https://github.com/user-attachments/assets/a5b6baf1-725a-48c6-905b-17e027460b56)

보정된 영상에서는 체스보드 위로 간단한 피라미드 모양이 보입니다. output.avi를 실행해 피라미드 모양의 AR 물체를 확인할 수 있습니다.
