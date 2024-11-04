from PyQt6.QtWidgets import *
import cv2 as cv
import numpy as np
import winsound
import sys

class Panorama(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('파노라마 영상')
        self.setGeometry(200, 200, 700, 200)
        
        collect_button = QPushButton('영상 수집', self)
        self.showButton = QPushButton('영상 보기', self)
        self.stitchButton = QPushButton('봉합', self)
        self.saveButton = QPushButton('저장', self)
        quitButton = QPushButton('종료', self)
        self.label = QLabel('환영합니다!', self)
    
        collect_button.setGeometry(10, 25, 100, 30)
        self.showButton.setGeometry(110, 25, 100, 30)
        self.stitchButton.setGeometry(210, 25, 100, 30)
        self.saveButton.setGeometry(310, 25, 100, 30)
        quitButton.setGeometry(450, 25, 100, 30)
        self.label.setGeometry(10, 70, 600, 170)
    
        self.showButton.setEnabled(False)
        self.stitchButton.setEnabled(False)
        self.saveButton.setEnabled(False)
    
        collect_button.clicked.connect(self.collectFunction)
        self.showButton.clicked.connect(self.showFunction)
        self.stitchButton.clicked.connect(self.stitchFunction)
        self.saveButton.clicked.connect(self.saveFunction)
        quitButton.clicked.connect(self.quitFunction)

    def collectFunction(self):
        self.showButton.setEnabled(False)
        self.stitchButton.setEnabled(False)
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
                self.imgs.append(frame) # 영상 저장
                winsound.Beep(1000, 100)
            elif key == ord('q'): 
                self.cap.release()
                cv.destroyAllWindows()
                break

        if len(self.imgs) >= 2: # 수집한 영상이 두 장 이상이면
            self.showButton.setEnabled(True)
            self.stitchButton.setEnabled(True)
            self.saveButton.setEnabled(True)

    def showFunction(self):
        self.label.setText('수집한 영상은 ' + str(len(self.imgs)) +  '장 입니다.')
        stack = cv.resize(self.imgs[0], dsize=(0, 0), fx=0.25, fy=0.25)
        for i in range(1, len(self.imgs)):
            stack = np.hstack((stack, cv.resize(self.imgs[i], dsize=(0, 0), fx=0.25, fy=0.25)))
        cv.imshow('Image collection', stack)

    def stitchFunction(self):
        stitcher = cv.Stitcher_create()
        status, self.img_stiched = stitcher.stitch(self.imgs)
        if status == cv.STITCHER_OK:
            cv.imshow('Image stiched panorama', self.img_stiched)
        else:
            winsound.Beep(3000, 500)
            self.label.setText('파노라마 제작에 실패했습니다. 다시 시도해주세요.')

    def saveFunction(self):
        if self.img_stiched is None:  # 이미지가 비어 있는지 확인(추가된 코드)
            self.label.setText('저장할 이미지가 없습니다.')
            return

        # fname = QFileDialog.getSaveFileName(self, '파일저장', './')
        # cv.imwrite(fname[0], self.img_stiched)

        fname = QFileDialog.getSaveFileName(self, '파일저장', './panorama.jpg')  # 기본 파일 이름 설정(추가된 코드)
        if fname[0]:  # 파일 이름이 선택되었는지 확인
            if not fname[0].endswith(('.jpg', '.jpeg', '.png')): # 확장자가 없으면 .jpg 추가
                fname = (fname[0] + '.jpg',)  # 기본 확장자 추가
            cv.imwrite(fname[0], self.img_stiched)

    def quitFunction(self):
        self.cap.release()
        cv.destroyAllWindows()
        self.close()

app = QApplication(sys.argv)
win = Panorama()
win.show()
app.exec()