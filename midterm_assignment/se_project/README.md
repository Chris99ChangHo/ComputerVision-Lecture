# 특수 효과 적용 프로그램

이 프로그램은 OpenCV와 PyQt6를 사용하여 사진과 비디오에 다양한 특수 효과를 적용할 수 있는 GUI 애플리케이션입니다.

## 주요 기능
- **사진 필터**: 엠보싱, 카툰, 연필 스케치, 유화 등의 필터를 적용할 수 있습니다.
- **비디오 필터**: 실시간으로 비디오 스트림에 특수 효과를 적용할 수 있습니다.
- **이미지 저장**: 선택한 필터가 적용된 이미지를 파일로 저장할 수 있습니다.
- **비교 모드**: 여러 필터가 적용된 결과를 한 화면에서 비교할 수 있습니다.

## 실행 방법
1. 가상 환경을 설정하고 활성화합니다.
  conda create -n ma python=3.11
  conda activate ma
2. 의존성을 설치합니다.
  pip install -r ./se_project/requirements.txt
3. 프로그램을 실행합니다.
  python ./src/make_specialeffect.py
  혹은 실행파일 make_specialeffect.exe