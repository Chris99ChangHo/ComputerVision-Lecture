from PyQt6.QtWidgets import *
import cv2 as cv
import numpy as np
import winsound
import sys

class Panorama(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('파노라마 영상')
        self.setGeometry(200, 200, 800, 300)  # 창 크기 조정

        # 버튼 생성
        collect_button = QPushButton('영상 수집', self)
        self.showButton = QPushButton('영상 보기', self)
        self.previewButton = QPushButton('미리보기', self)  # 미리보기 버튼
        self.stitchButton = QPushButton('봉합', self)
        self.editButton = QPushButton('이미지 편집', self)  # 이미지 편집 버튼
        self.saveButton = QPushButton('저장', self)
        quitButton = QPushButton('종료', self)
        self.label = QLabel('환영합니다!', self)

        # 버튼 위치 설정
        collect_button.setGeometry(10, 25, 100, 30)
        self.showButton.setGeometry(120, 25, 100, 30)
        self.previewButton.setGeometry(230, 25, 100, 30) # 미리보기 버튼 위치 설정
        self.stitchButton.setGeometry(340, 25, 100, 30)
        self.editButton.setGeometry(450, 25, 100, 30)  # 이미지 편집 버튼 위치 설정
        self.saveButton.setGeometry(560, 25, 100, 30)
        quitButton.setGeometry(670, 25, 100, 30)
        self.label.setGeometry(10, 70, 780, 200)

        # 버튼 활성화 상태 설정
        self.showButton.setEnabled(False)
        self.previewButton.setEnabled(False) # 미리보기 버튼 비활성화
        self.stitchButton.setEnabled(False)
        self.editButton.setEnabled(False)  # 이미지 편집 버튼 비활성화
        self.saveButton.setEnabled(False)

        # 버튼 클릭 시 연결될 함수 설정
        collect_button.clicked.connect(self.collectFunction)
        self.showButton.clicked.connect(self.showFunction)
        self.previewButton.clicked.connect(self.previewFunction) # 미리보기 함수 연결
        self.stitchButton.clicked.connect(self.stitchFunction)
        self.editButton.clicked.connect(self.editFunction)  # 이미지 편집 기능 연결
        self.saveButton.clicked.connect(self.saveFunction)
        quitButton.clicked.connect(self.quitFunction)

    def collectFunction(self):
        self.showButton.setEnabled(False)
        self.previewButton.setEnabled(False)
        self.stitchButton.setEnabled(False)
        self.editButton.setEnabled(False)
        self.saveButton.setEnabled(False)
        self.label.setText('c를 여러 번 눌러 수집하고 끝나면 q를 눌러 비디오를 끕니다')

        self.cap = cv.VideoCapture(0, cv.CAP_DSHOW)
        if not self.cap.isOpened(): sys.exit('카메라 연결 실패')

        self.imgs = []
        while True:
            ret, frame = self.cap.read()
            if not ret: break
            cv.imshow('video display', frame)

            key = cv.waitKey(1)
            if key == ord('c'):
                self.imgs.append(frame)  # 영상 저장
                winsound.Beep(1000, 100)
            elif key == ord('q'):
                self.cap.release()
                cv.destroyAllWindows()
                break

        if len(self.imgs) >= 2:  # 수집한 영상이 두 장 이상이면
            self.showButton.setEnabled(True)
            self.previewButton.setEnabled(True)
            self.stitchButton.setEnabled(True)

    def showFunction(self):
        self.label.setText('수집한 영상은 ' + str(len(self.imgs)) + '장 입니다.')
        stack = cv.resize(self.imgs[0], dsize=(0, 0), fx=0.25, fy=0.25)
        for i in range(1, len(self.imgs)):
            stack = np.hstack((stack, cv.resize(self.imgs[i], dsize=(0, 0), fx=0.25, fy=0.25)))
        cv.imshow('Image collection', stack)

    def previewFunction(self):
        self.label.setText('파노라마 미리보기 중입니다...')
        stitcher = cv.Stitcher_create()
        status, preview = stitcher.stitch(self.imgs)
        if status == cv.STITCHER_OK:
            cv.imshow('Panorama Preview', preview)  # 미리보기 이미지 표시
        else:
            winsound.Beep(3000, 500)
            self.label.setText('미리보기에 실패했습니다. 다시 시도해주세요.')

    def stitchFunction(self):
        self.label.setText('이미지를 봉합 중입니다...')
        stitcher = cv.Stitcher_create()
        status, self.img_stiched = stitcher.stitch(self.imgs)
        if status == cv.STITCHER_OK:
            cv.imshow('Stitched Panorama', self.img_stiched)
            self.editButton.setEnabled(True)  # 편집 버튼 활성화
            self.saveButton.setEnabled(True)
        else:
            winsound.Beep(3000, 500)
            self.label.setText('파노라마 제작에 실패했습니다. 다시 시도해주세요.')

    def editFunction(self):
        self.label.setText('이미지 편집 중입니다...') 
        if self.img_stiched is None:
            self.label.setText('편집할 이미지가 없습니다.')
            return

        h, w = self.img_stiched.shape[:2]
        cropped_img = self.img_stiched[50:h-50, 50:w-50]  # Numpy 슬라이싱을 이용한 이미지 자르기

        # 밝기 조정: alpha는 대비, beta는 밝기
        alpha = 1.2  # 대비 (1.0은 원본 대비, 더 높은 값은 더 높은 대비)
        beta = 50    # 밝기 (0은 원본 밝기, 더 높은 값은 더 밝게)
        adjusted_img = cv.convertScaleAbs(cropped_img, alpha=alpha, beta=beta)

        self.img_stiched = adjusted_img
        cv.imshow('Edited Panorama', self.img_stiched)
        self.label.setText('이미지 편집이 완료되었습니다.')

    def saveFunction(self):
        if self.img_stiched is None:
            self.label.setText('저장할 이미지가 없습니다.')
            return

        fname = QFileDialog.getSaveFileName(self, '파일저장', './pano_img/panorama.jpg')
        if fname[0]:
            if not fname[0].endswith(('.jpg', '.jpeg', '.png')):
                fname = (fname[0] + '.jpg',)
            cv.imwrite(fname[0], self.img_stiched)
            self.label.setText('이미지가 성공적으로 저장되었습니다.')

    def quitFunction(self):
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        cv.destroyAllWindows()
        self.close()

app = QApplication(sys.argv)
win = Panorama()
win.show()
app.exec()
