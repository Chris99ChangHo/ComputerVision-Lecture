import cv2 as cv
import numpy as np
from PyQt6.QtWidgets import *
import sys
import os

class SpecialEffect(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('비디오 특수 효과')
        self.setGeometry(200, 200, 800, 500)

        # 사진 관련 버튼
        photo_label = QLabel('사진 필터', self)
        photo_label.setGeometry(10, 10, 200, 20)
        picture_button = QPushButton('사진 읽기', self)
        emboss_button = QPushButton('엠보싱', self)
        cartoon_button = QPushButton('카툰', self)
        sketch_button = QPushButton('연필 스케치', self)
        oil_button = QPushButton('유화', self)
        save_button = QPushButton('저장하기', self)
        self.pickCombo = QComboBox(self)
        self.pickCombo.addItems(['엠보싱', '카툰', '연필 스케치(명암)', '연필 스케치(컬러)', '유화'])
        quit_button = QPushButton('나가기', self)
        compare_button = QPushButton('비교 모드', self)  # 비교 모드 버튼

        # 레이블 추가 (완료 메시지를 출력하기 위한 레이블)
        self.label = QLabel(self)
        self.label.setGeometry(10, 120, 780, 30)

        # 비디오 관련 버튼
        video_label = QLabel('비디오 필터', self)
        video_label.setGeometry(10, 300, 200, 20)
        start_video_button = QPushButton('비디오 시작', self)
        self.videoCombo = QComboBox(self)
        self.videoCombo.addItems(['엠보싱', '카툰', '연필 스케치(명암)', '유화'])
        stop_video_button = QPushButton('비디오 종료', self)

        # 사진 버튼 레이아웃
        picture_button.setGeometry(10, 40, 100, 30)
        emboss_button.setGeometry(120, 40, 100, 30)
        cartoon_button.setGeometry(230, 40, 100, 30)
        sketch_button.setGeometry(340, 40, 100, 30)
        oil_button.setGeometry(450, 40, 100, 30)
        save_button.setGeometry(560, 40, 100, 30)
        self.pickCombo.setGeometry(560, 80, 110, 30)
        quit_button.setGeometry(670, 40, 100, 30)
        compare_button.setGeometry(10, 80, 100, 30)  # 비교 모드 버튼 레이아웃

        # 비디오 버튼 레이아웃
        start_video_button.setGeometry(10, 330, 100, 30)
        self.videoCombo.setGeometry(120, 330, 100, 30)
        stop_video_button.setGeometry(230, 330, 100, 30)

        # 사진 관련 버튼 연결
        picture_button.clicked.connect(self.pictureOpenFunction)
        emboss_button.clicked.connect(self.embossFunction)
        cartoon_button.clicked.connect(self.cartoonFunction)
        sketch_button.clicked.connect(self.sketchFunction)
        oil_button.clicked.connect(self.oilFunction)
        save_button.clicked.connect(self.saveFunction)
        quit_button.clicked.connect(self.quitFunction)
        compare_button.clicked.connect(self.compareFunction)  # 비교 모드 버튼 연결

        # 비디오 관련 버튼 연결
        start_video_button.clicked.connect(self.startVideo)
        stop_video_button.clicked.connect(self.stopVideo)

        self.cap = None  # 비디오 캡처 객체 초기화

    def pictureOpenFunction(self):
        fname = QFileDialog.getOpenFileName(self, '사진 읽기', './se_img/')
        self.img = cv.imread(fname[0])
        if self.img is None: sys.exit('파일을 찾을 수 없습니다.')
        cv.imshow('Painting', self.img)

    def embossFunction(self):
        femboss = np.array([[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
        gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        gray16 = np.int16(gray)
        self.emboss = np.uint8(np.clip(cv.filter2D(gray16, -1, femboss) + 128, 0, 255))
        cv.imshow('Embossing', self.emboss)

    def cartoonFunction(self):
        self.cartoon = cv.stylization(self.img, sigma_s=60, sigma_r=0.45)
        cv.imshow('Cartoon', self.cartoon)

    def sketchFunction(self):
        self.sketch_gray, self.sketch_color = cv.pencilSketch(self.img, sigma_s=60, sigma_r=0.07, shade_factor=0.02)
        cv.imshow('pencil Sketch(gray)', self.sketch_gray)
        cv.imshow('pencil Sketch(color)', self.sketch_color)

    def oilFunction(self):
        self.oil = cv.xphoto.oilPainting(self.img, 10, 1, cv.COLOR_BGR2LAB)
        cv.imshow('Oil Painting', self.oil)

    def compareFunction(self):
        if self.img is None:
            self.label.setText("이미지를 먼저 불러와 주세요.")
            return

        # 각 필터 적용
        femboss = np.array([[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
        gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        gray16 = np.int16(gray)
        emboss = np.uint8(np.clip(cv.filter2D(gray16, -1, femboss) + 128, 0, 255))
        cartoon = cv.stylization(self.img, sigma_s=60, sigma_r=0.45)
        sketch_gray, _ = cv.pencilSketch(self.img, sigma_s=60, sigma_r=0.07, shade_factor=0.02)
        oil = cv.xphoto.oilPainting(self.img, 10, 1, cv.COLOR_BGR2LAB)

        # 이미지를 병합하여 비교
        combined = np.hstack((
            self.img,
            cv.cvtColor(emboss, cv.COLOR_GRAY2BGR),
            cartoon,
            cv.cvtColor(sketch_gray, cv.COLOR_GRAY2BGR),
            oil
        ))

        cv.imshow('All Filters Comparison', combined)

    def saveFunction(self):
        # 저장 경로 및 필터 이름 설정
        base_path = './se_img/saved_image'
        extension = '.jpg'
        filter_names = ['embossing', 'cartoon', 'sketch_gray', 'sketch_color', 'oil_painting']

        # 선택한 필터 이름 가져오기
        i = self.pickCombo.currentIndex()
        filter_name = filter_names[i]

        # 최종 파일 이름 생성
        fname = f"{base_path}_{filter_name}{extension}"

        # 선택한 필터에 따라 이미지 저장
        image_to_save = None
        if i == 0:
            image_to_save = self.emboss
        elif i == 1:
            image_to_save = self.cartoon
        elif i == 2:
            image_to_save = self.sketch_gray
        elif i == 3:
            image_to_save = self.sketch_color
        elif i == 4:
            image_to_save = self.oil

        if image_to_save is None:
            self.label.setText('필터를 적용한 후에 저장해 주세요.')
            return

        # 이미지 저장
        cv.imwrite(fname, image_to_save)
        self.label.setText('이미지가 성공적으로 저장되었습니다.')

    def startVideo(self):
        self.cap = cv.VideoCapture(0)
        if not self.cap.isOpened():
            print("웹캠을 열 수 없습니다.")
            return
        self.runVideoLoop()

    def runVideoLoop(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            # 비디오 필터 선택에 따라 적용
            filter_index = self.videoCombo.currentIndex()
            if filter_index == 0:  # 엠보싱 필터
                femboss = np.array([[-1.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]])
                gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                gray16 = np.int16(gray)
                frame = np.uint8(np.clip(cv.filter2D(gray16, -1, femboss) + 128, 0, 255))
                frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
            elif filter_index == 1:  # 카툰 필터
                frame = cv.stylization(frame, sigma_s=60, sigma_r=0.45)
            elif filter_index == 2:  # 연필 스케치(명암) 필터
                frame, _ = cv.pencilSketch(frame, sigma_s=60, sigma_r=0.07, shade_factor=0.02)
                frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR)
            elif filter_index == 3:  # 유화 필터
                frame = cv.xphoto.oilPainting(frame, 10, 1, cv.COLOR_BGR2LAB)

            cv.imshow('Filtered Video', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    def stopVideo(self):
        if self.cap:
            self.cap.release()
            cv.destroyAllWindows()

    def quitFunction(self):
        self.stopVideo()
        self.close()

app = QApplication(sys.argv)
window = SpecialEffect()
window.show()
app.exec()
