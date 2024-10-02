# 기본 패키지?
import sys
# from collections import defaultdict
# import itertools

# 다운받은 패키지
import cv2

# 내가만든 패키지
# import ~~~

# img = cv2.imread("./cat.jpg")  # 경로 정확하게 확인 해야함
img = cv2.imread("./assets/cat.jpg")
if img is None:
    sys.exit("파일을 찾을 수 없습니다.")

cv2.imshow("Image Display", img)
cv2.waitKey()
cv2.destroyAllWindows()
