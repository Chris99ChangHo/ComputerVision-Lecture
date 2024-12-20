# 파노라마 생성 프로그램

이 프로그램은 OpenCV와 PyQt6를 사용하여 여러 이미지를 수집하고, 봉합하여 파노라마 이미지를 생성하는 GUI 애플리케이션입니다.

## 주요 기능
- **영상 수집**: 카메라를 통해 이미지를 수집합니다.
- **미리보기**: 수집한 이미지들을 봉합하기 전에 미리 확인할 수 있습니다.
- **이미지 봉합**: 이미지를 봉합하여 파노라마를 생성합니다.
- **이미지 편집**: 생성된 파노라마 이미지를 자르거나 밝기, 색상 보정을 수행합니다.
- **저장**: 편집된 이미지를 파일로 저장합니다.

## 실행 방법
1. 가상 환경을 설정하고 활성화합니다.
  conda create -n ma python=3.11
  conda activate ma 
2. 의존성을 설치합니다.
  pip install -r ./pano_project/requirements.txt
3. 프로그램을 실행합니다.
  python ./src/make_panorama.py
  혹은 실행파일 make_panorama.exe
